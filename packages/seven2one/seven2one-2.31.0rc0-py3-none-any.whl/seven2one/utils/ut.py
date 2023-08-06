
from dataclasses import dataclass
import pytz
import os
import base64
import pandas as pd
from gql import gql
from tzlocal import get_localzone
from loguru import logger
from collections import namedtuple

if os.name == 'nt': #only if the platform is Windows, pyperclip will be imported
    import pyperclip

@dataclass
class Defaults():
    timeZone: str = 'UTC'
    useDateTimeOffset: bool = True
    copyGraphQLString: bool = False
    includeSystemProperties: bool = False

class Structure():
    queryStructure = f'''query inventories {{
    inventories (pageSize:1000) {{
        name
        inventoryId
        displayValue
        isDomainUserType
        hasValidityPeriods
        historyEnabled
        propertyUniqueness {{
            uniqueKey
            properties
            }}
        variant {{
            name
            properties {{
                name
                type
                isArray
                nullable
                }}
            }}
        properties {{
            name
            ...Scalar
            type
            isArray
            nullable
            propertyId
            ... Reference 
            }}
        }}
    }}
    fragment Scalar on IScalarProperty {{
        dataType
        }}
    fragment Reference on IReferenceProperty {{
        inventoryId
        inventoryName
        }}
    '''

    def _introspectionQueryString():
        introspectionQueryString = r'''
            query IntrospectionQuery { __schema { queryType { name } mutationType 
                { name } subscriptionType { name } types { ...FullType } directives
                { name description locations args { ...InputValue } } } }

            fragment FullType on __Type { kind name description fields(includeDeprecated: true) { name description args 
                { ...InputValue } type { ...TypeRef } isDeprecated deprecationReason } inputFields { ...InputValue } interfaces 
                { ...TypeRef } enumValues(includeDeprecated: true) { name  } possibleTypes { ...TypeRef } } 

            fragment InputValue on __InputValue { name description type { ...TypeRef } defaultValue } 
            fragment TypeRef on __Type { kind name ofType { kind name ofType { kind name ofType 
                    { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name } } } } } } } }
        '''
        return introspectionQueryString

    def _fullStructureDict(structure) -> dict:
        """Converts the query of all inventories with all fields into a pure dict"""

        def subdict(inputObject, name):
            itemDict = {}
            for item in inputObject:
                itemDict.setdefault(item[name], {})
                for k, v in item.items():
                    itemDict[item[name]].setdefault(k,v)
            return itemDict

        structureDict = {}
        for inventory in structure['inventories']:
            inventoryName = inventory['name']
            structureDict.setdefault(inventoryName, {})
            for definitionKey, definitionValue in inventory.items():
                if not isinstance(definitionValue, (list, dict)):
                    structureDict[inventoryName].setdefault(definitionKey, definitionValue)
                else:
                    if definitionKey == 'properties':
                        subDict = subdict(inventory[definitionKey], 'name')
                        structureDict[inventoryName].setdefault(definitionKey, subDict)
                    if definitionKey == 'propertyUniqueness':
                        subDict = subdict(inventory[definitionKey], 'uniqueKey')
                        structureDict[inventoryName].setdefault(definitionKey, subDict)
                    if definitionKey == 'variant':
                        structureDict[inventoryName].setdefault(definitionKey, {})
                        structureDict[inventoryName][definitionKey].setdefault('name', definitionValue['name'])
                        subDict = subdict(inventory[definitionKey]['properties'], 'name')
                        structureDict[inventoryName][definitionKey].setdefault('properties', subDict)
        return structureDict

    def _fullStructureNT(structure:dict) -> namedtuple:
        """
        Provides the complete data structure of dynamic objects as named tuple. 
        Needs structureDict first
        """
        def _subItem(object:dict):
            Item = namedtuple('Item', object.keys())
            itemDict = {}
            for key, value in object.items():
                if isinstance(value, dict):
                    subItem = _subItem(value)
                    itemDict.setdefault(key, subItem)
                else:
                    itemDict.setdefault(key, value)
            item = Item(**itemDict)
            return item

        Item = namedtuple('Item', structure.keys())
        itemDict = {}
        for key, value in structure.items():
            if isinstance(value, dict):
                subItem = _subItem(value)
                itemDict.setdefault(key, subItem)
            else:
                itemDict.setdefault(key, value)
        return Item(**itemDict)

    def _inventoryNT(structure) -> namedtuple:
        """
        Provides a simplified namedtuple of dynamic objects for interactive usage
        """
        inventoryDict = {key:key for key in structure.keys()}
        Inventories = namedtuple('Inventories', inventoryDict.keys())
        return Inventories(**inventoryDict)

    def _inventoryPropertyNT(structure) -> namedtuple:
        """
        Provides a simplified namedtuple of inventory properties for interactive usage
        """
        Inventory = namedtuple('Inventories', structure.keys())
        inventoryDict = {}

        for inventory in structure.keys():
            propertyDict = {}
            for key in structure[inventory]['properties'].keys():
                propertyDict.setdefault(key, key)
                Properties = namedtuple('Properties', propertyDict.keys())
                properties = Properties(**propertyDict)
            inventoryDict.setdefault(inventory, properties)
        return Inventory(**inventoryDict)

class Utils():
    errors =  f'''errors {{
                    message
                    code
                }}'''

    def _error(self, msg:str):
        if self.raiseException: raise Exception(msg)
        else:
            logger.error(msg)
            return

    def _timeZone(timeZone):
        if timeZone=='local': 
            localTimeZone = get_localzone().zone
            return str(pytz.timezone(localTimeZone))
        else:
            return str(pytz.timezone(timeZone))
    
    def _queryFields(fieldList:list, arrayTypeFields:list=None, arrayPageSize:int=None, recursive=False) -> str:
        """
        Transforms a Python list of fields into graphQL String of fields
        including fields of referenced inventories        
        """
        fields = ''
        splitList = [item.split('.') for item in fieldList]
        logger.debug(f"intermediate step - splitted list: {splitList}")

        def nestedItem(item):
            nonlocal fields
            line = ''
            for i in range(itemLength - 1):
                if arrayTypeFields != None and item[i] in arrayTypeFields:
                    line += f'{item[i]} (pageSize: {arrayPageSize}) {{ '
                else:
                    line += f'{item[i]} {{ '
            line += f'{item[-1]} '
            for _ in range(itemLength - 1):
                line += '}'
            line += ' \n'
            fields += line
    
        for item in splitList:
            if len(item) == 1:
                fields += f'{item[0]}  \n'
            else:
                itemLength = len(item)
                if recursive == False:
                    if item[-1] == '_displayValue':  
                        nestedItem(item)
                    if item[-1] == 'sys_inventoryItemId':  
                        nestedItem(item)
                else:
                    nestedItem(item)
        return fields
   
    def _resolveWhereString(self, filterString):
        """
        How does this work:
        A list of lists is created, where 'or terms' are the elements of the parent list and 
        'and terms' are elements of a child list of an or (or single) element.
        For each 'and' in a child list, the string will be closed with an extra '}'

        Lists (as string) are treated seperately, but work the same as a single or an 'and' element.

        """

        def mapOperator(operator):
            operators = {
                '==': 'eq',
                'eq': 'eq',
                'in': 'in',
                '<': 'lt',
                '>': 'gt',
                '<=': 'lte',
                '>=': 'gte',
                'lt': 'lt',
                'gt': 'gt',
                'lte': 'lte',
                'gte': 'gte',
                'contains': 'contains',
                '!=': 'ne',
                'not in': 'not in',
                'startswith': 'startswith',
                'endswith': 'endswith',
                '=': 'eq'
            }
            if operator in operators:
                return operators[operator]
            else:
                logger.error(f"Unknown operator '{operator}'")

        def _createStringList(itemList:list) -> str:
            result = '['
            for item in itemList:
                result += f'"{item}",'
            result += ']'
            return result

        def _secondLevelFilter(split:list, lastElement:str):
            subProperty = split[0].split('.')[0]
            subFilterProperty = split[0].split('.')[1]
            subInventory = self.structure['ZSEnext']['properties'][subProperty]['inventoryName']
            df = self.items(subInventory, fields=['sys_inventoryItemId'], 
                where=f'{subFilterProperty} {split[1]} {lastElement}')

            itemIds = list(df['sys_inventoryItemId'])
            if len(itemIds) == 0:
                logger.error(f"{split[0]} is not a valid filter criteria.")
            elif len(itemIds) == 1:
                whereString = f'{subProperty}: {{sys_inventoryItemId: {{ {mapOperator(split[1])}: "{itemIds[0]}" }} }}'
            else: # if it is a list
                itemIds = _createStringList(itemIds)
                whereString = f'{subProperty}: {{sys_inventoryItemId: {{ {mapOperator(split[1])}: {itemIds} }} }}'
            return whereString         

        # Clean string
        filterString = filterString.replace('  ', ' ')

        # Create list of lists
        orElements = filterString.split(' or ')
        filterElements = [e.split(' and ') for e in orElements]
        logger.debug(f"where-elements: {filterElements}")

        # Create GraphQL String
        graphQlElements = 'where: { '

        for i, element in enumerate(filterElements):
            for j, subElement in enumerate(element):
                if '[' in subElement: # Checks if, if search string is a list
                    x = subElement.find('[')
                    split = subElement[:x].split(' ')
                    if split[0].count('.') == 1:
                        whereString = _secondLevelFilter(split, subElement[x:])
                    else:
                        whereString = f'{split[0]}: {{ {mapOperator(split[1])}: {subElement[x:]} }}'
                else:
                    if subElement.count('"') == 1: # Error, not possible
                        logger.error(f'''Search strings must be enclosed by '"'. ''')
                    elif subElement.count('"') == 0: # Search string is a number
                        split = subElement.split(' ')
                        whereString = f'{split[0]}: {{ {mapOperator(split[1])}: {split[2]} }}'
                    elif subElement.count('"') == 2: # Search string is a string
                        y = subElement.find('"')
                        lastElement = subElement[y:]
                        split = subElement[:y].split(' ')
                        if split[0].count('.') == 1:
                            whereString = _secondLevelFilter(split, lastElement)
                        else:
                            whereString = f'{split[0]}: {{ {mapOperator(split[1])}: {split[2] + lastElement} }}'
                    else:
                        logger.error(f'''Filter elements with search strings may only contain 2 '"'. ''')
                graphQlElements += whereString
                if j == len(element) - 1:
                    if len(element) > 1:
                        for _ in range(j):
                            graphQlElements += ' } '
                    break
                graphQlElements += ' and: {'

            if i == len(filterElements) - 1: 
                graphQlElements += ' } '

                break
            graphQlElements += ' or: {'
        if len(filterElements) > 1:
            graphQlElements += ' }'

        return graphQlElements

    def _propertiesToString(properties:list) -> str:
        """ Converts a list of property dicts for many items into a string """
        if type(properties) == list:
            _properties = '[\n'
            for property in properties:
                _properties += '{\n'
                for key, value in property.items():
                    _properties += Utils._customProperties(key, value)      
                
                _properties += '}\n'
            _properties += ']'
            return _properties
        if type(properties) == dict:
            _properties = '{\n'
            for key, value in properties.items():
                _properties += Utils._customProperties(key, value)
            _properties += '}\n'
            return _properties
        else:
            logger.error(f"Type of property items has to be either list ord dict.")
            return

    def _tsPropertiesToString(properties:list) -> str:
        """ Converts a list of property dicts for many items into a string """
        timeUnit, factor = 'timeUnit', 'factor'
        _properties = '[\n'
        for property in properties:
            _properties += '{\n'
            for key, value in property.items():
                if key == 'resolution':
                    try:
                        _properties += f'{key}: {{\n'
                        _properties += f'timeUnit: {value[timeUnit]}\n'
                        _properties += f'factor: {value[factor]}\n'
                        _properties += f'}}\n'
                    except KeyError:
                        logger.error("Missing 'timeUnit' and/or 'factor' for Timeseries resolution")
                        return
                else:
                    _properties += Utils._customProperties(key, value)
            
            _properties += '}\n'
        _properties += ']'
        return _properties

    def _addToGroupPropertiesToString(groupItemId:str, properties:list) -> str:
        """ Converts a list of property dicts for many items into a string """
        
        _properties = '[\n'
        for property in properties:
            _properties += f'{{sys_groupInventoryItemId: "{groupItemId}"\n'
            for key, value in property.items():
                _properties += Utils._customProperties(key, value)      
            
            _properties += '}\n'
        _properties += ']'
        return _properties

    def _uniquenessToString(propertyUniqueness: list):
        """ Converts a list of unique keys into a string """    

        _uniqueKeys = '[\n'
        for item in propertyUniqueness:
            key = item['uniqueKey']
            _uniqueKeys += f'{{uniqueKey: "{key}" properties: ['
            for value in item['properties']:
                _uniqueKeys += f'"{value}",'     
            
            _uniqueKeys += ']}\n'
        _uniqueKeys += ']'
        return _uniqueKeys

    def _customProperties(key:str, value:object) -> str:

        """Used internally (in Utils) as helper function"""

        _propertyString = ''
        if key == 'dataType':
            _propertyString += f'{key}: {value}\n'
        elif type(value) == str:
            if len(value) >= 64 or '\n' in value or '"' in value:
                _propertyString += f'{key}: """{value}"""\n'
            else: 
                _propertyString += f'{key}: "{value}"\n'
        elif type(value) == int or type(value) == float:
            _propertyString += f'{key}: {value}\n'
        elif type(value) == bool:
            if value == True: _propertyString += f'{key}: true\n'
            if value == False: _propertyString += f'{key}: false\n'
        elif type(value) == list:
            _value = '['
            for element in value:
                if type(element) == int or type(element) == float:
                    _value += f'{element}, '
                elif type(element) == bool:
                    if element == True: element = 'true'
                    if element == False: element = 'false'
                    _value += f'{element}, '
                else:
                    _value += f'"{element}", '
            _propertyString += f'{key}: {_value}]\n'
        elif value == None:
            _propertyString += f'{key}: null\n'
        else:
            logger.error(f"{value} is an unsupported value type.")

        return _propertyString

    def _properties(scheme, inventoryName:str, recursive:bool=True, sysProperties:bool=False) -> dict:
        """
        Creates a nested (or unnested) dict with properties and arra 
        type fields for further usage out of the scheme
        """

        propertyDict = {'properties':{}, 'arrayTypeFields':[]}
        properties = propertyDict['properties']
        arrayTypeFields = propertyDict['arrayTypeFields']

        def _getInventoryObject(scheme, inventoryName):
            for item in scheme['__schema']['types']:
                if item['name'] == inventoryName:
                    return item['fields']
        
        def _createSubDict(subInv):
            subDict = {}
            inventoryObject = _getInventoryObject(scheme, subInv)
            for item in inventoryObject:
                if sysProperties == False:
                    if item['name'].startswith('sys_'):
                        if item['name'] == 'sys_inventoryItemId': pass
                        else: continue
                if item['type']['kind'] == 'SCALAR':
                    subDict.setdefault(item['name'], item['type']['name'])
                if item['type']['kind'] == 'LIST':
                    if item['name'] == 'sys_permissions': pass
                    elif item['type']['ofType']['kind'] == 'OBJECT':
                        arrayTypeFields.append(item['name'])
                        if recursive == False:
                            subDict.setdefault(item['name'], item['type']['name'])
                        else:
                            subDict.setdefault(item['name'], _createSubDict(item['type']['ofType']['name']))
                    else:
                        arrayTypeFields.append(item['name'])
                        subDict.setdefault(item['name'], item['type']['name'])
                if item['type']['kind'] == 'OBJECT':
                    if recursive == False:
                        subDict.setdefault(item['name'], item['type']['name'])
                    else:
                        subDict.setdefault(item['name'], _createSubDict(item['type']['name']))

            return subDict

        inventoryObject = _getInventoryObject(scheme, inventoryName)
        for item in inventoryObject:
            if sysProperties == False:
                if item['name'].startswith('sys_'):
                    if item['name'] == 'sys_inventoryItemId': pass
                    else: continue
            if item['type']['kind'] == 'SCALAR':
                properties.setdefault(item['name'], item['type']['name'])
            if item['type']['kind'] == 'LIST':
                if item['name'] == 'sys_permissions': pass
                elif item['type']['ofType']['kind'] == 'OBJECT':
                    arrayTypeFields.append(item['name'])
                    if recursive == False:
                        properties.setdefault(item['name'], item['type']['name'])
                    else:
                        properties.setdefault(item['name'], _createSubDict(item['type']['ofType']['name']))
                else:
                    arrayTypeFields.append(item['name'])
                    properties.setdefault(item['name'], item['type']['name'])
            if item['type']['kind'] == 'OBJECT':
                if recursive == False:
                    properties.setdefault(item['name'], item['type']['name'])
                else:
                    properties.setdefault(item['name'], _createSubDict(item['type']['name']))

        logger.debug(f"returned property dict: {propertyDict}")
        
        return propertyDict


    def _propertyList(propertyDict:dict, recursive:bool=False) -> list:
        """Uses _properties() to create a flat list of properties"""

        propertyList = []
    
        def instDict(subDict, path):
            if recursive == True:
                for k, v in subDict.items():
                    if isinstance(v, dict):
                        path = f'{path}.{k}'
                        instDict(subDict[k], path)
                    else:
                        propertyList.append(f'{path}.{k}')
            else:
                if '_displayValue' in subDict.keys(): #if it is not an array
                    propertyList.append(f'{path}._displayValue')
                else: # if it is an array
                    propertyList.append(f'{path}.sys_inventoryItemId')

        for k, v in propertyDict.items():
            if isinstance(v, dict):
                instDict(propertyDict[k], k)
            else:
                propertyList.append(k)

        logger.debug(f'returend property list: {propertyList}')
        return propertyList
            
    def _propertyTypes(propertyDict:dict) -> dict:
        """Uses _properties() o create a flat dictionary of properties"""

        propertyTypes = {}
        
        def instDict(subDict, path):
            for k, v in subDict.items():
                if isinstance(v, dict):
                    path = f'{path}.{k}'
                    instDict(subDict[k], path)
                else:
                    propertyTypes.setdefault(f'{path}.{k}', v)

        for k, v in propertyDict.items():
            if isinstance(v, dict):
                instDict(propertyDict[k], k)
            else:
                propertyTypes.setdefault(k, v)

        logger.debug(f"returned property types: {propertyTypes}")
        return propertyTypes
        
    def _copyGraphQLString(graphQLString:str, copyGraphQLString:bool=False) -> None:
        """Can be applied to any core function to get the GraphQL string which is stored in the clipboard"""
        if copyGraphQLString == True and os.name == 'nt':
           return pyperclip.copy(graphQLString)

    def _getVariantId(variants:pd.DataFrame, name:str) -> str:
        """ Gets the variant Id from a given name""" 
        variants.set_index('name', inplace=True)
        return variants.loc[name][0]

    def _listGraphQlErrors(result:dict, key:str) -> None:
        """Print errors from GraphQL Query to log"""
        
        for i in result[key]['errors']:
            logger.error(i['message'])

    def _encodeBase64(file:str):
        with open(file) as file:
            content = file.read()
            content = base64.b64encode(content.encode('ascii'))
            return content.decode('UTF8')

    # deprecated:
    def _getInventoryId(self, inventoryName):
        inventory = self.inventories(where=f'name eq "{inventoryName}"')
        
        if inventory.empty:
            msg = f"Unknown inventory '{inventoryName}'."
            if self.raiseException: raise Exception(msg)
            else:
                logger.error(msg)
                return

        inventoryId = inventory.loc[0, 'inventoryId']
        logger.debug(f'returned inventory id: {inventoryId}')
        return inventoryId        

    def _arrayItemsToString(arrayItems:list, operation:str, cascadeDelete:bool) -> str:
        """Converts a list of array items to a graphQL string"""

        cDelValue = 'true' if cascadeDelete == True else 'false'

        if operation == 'insert':
            _arrayItems = 'insert: [\n'
            for item in arrayItems:
                _arrayItems += f'{{value: "{item}"}}\n'
            _arrayItems += ']'
            return _arrayItems
        if operation == 'removeByIndex':
            _arrayItems = f'cascadeDelete: {cDelValue}\n'
            _arrayItems += 'removeByIndex: ['
            for item in arrayItems:
                _arrayItems += f'{item}, '
            _arrayItems += ']'
            return _arrayItems
        if operation == 'removeById':
            _arrayItems = f'cascadeDelete: {cDelValue}\n'
            _arrayItems += 'removeById: ['
            for item in arrayItems:
                _arrayItems += f'"{item}", '
            _arrayItems += ']'
            return _arrayItems
        if operation == 'removeAll':
            _arrayItems = f'cascadeDelete: {cDelValue}\n'
            _arrayItems += 'removeByIndex: ['
            for item in arrayItems:
                _arrayItems += f'{item}, '
            _arrayItems += ']'
            return _arrayItems

    def _executeGraphQL(self, graphQLString):
        """Executes GraphQl, this code is used in every main function"""

        Utils._copyGraphQLString(graphQLString, self.defaults.copyGraphQLString)      
        logger.trace(f"GraphQLString: {graphQLString}")
        try:
            query = gql(graphQLString)
        except Exception as err:
            if self.raiseException: raise Exception(err)
            else:
                logger.error(err)
                return

        try:
            result = self.client.execute(query)
        except Exception as err:
            if self.raiseException: raise Exception(err)
            else:
                logger.error(err)
                return
        
        return result

    def _argNone(arg, value, enum=False) -> str:
        """
        Creates a simple string (to be embedded in graphQlString) 
        for arguments that are None by default.
        """
        if value == None:
            return ''
        else:
            if enum == True:
                return f'{arg}: {value}'
            else:
                if type(value) == str:
                    return f'{arg}: "{value}"'
                elif type(value) == float:
                    return f'{arg}: {value}'
                elif type(value) == int:
                    return f'{arg}: {value}'
                elif type(value) == bool:
                    if value == True:
                        return f'{arg}: true'
                    else:
                        return f'{arg}: false'
                else:
                    return f'{arg}: "{str(value)}"'
