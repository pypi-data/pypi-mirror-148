import json
from json.decoder import JSONDecodeError
class JsonObjectManager:
    # allowed attributes is a list contains wich  attributes you allowed to be added in this object
    # the Class will not append any other attribute that is out of this list 
    # default: all the keys in your data object 
    # you can not disallow any key that is in your data object 
    allowed = []
    def __init__(self,data,allowed=[]):
        # object data -> str(Json Object) | list(Any) | dict(key&value)
        self._data = data
        # instance controler -> dict : handled by the instance 
        self._object = None
        # desc in the top ^ 
        self.allowed = allowed
        # instance keys 
        self._keys = []
        # handle data object 
        self._handle_data()

    def valid(self):
        try:
            json.loads(self.data)
            return True
        except JSONDecodeError:
            return False

    # handle data object 
    def _handle_data(self):
        if isinstance(self._data,str) and isinstance(json.loads(self._data),dict):
            self._object = {}
            keys = json.loads(self._data)
            for key,val in keys.items():
                self._object[key] = val
                self._keys.append(key)

        elif  isinstance(self._data,dict):
            self._object = {}
            keys = self._data
            for key,val in keys.items():
                self._object[key] = val
                self._keys.append(key)


        elif isinstance(self._data,str) and isinstance(json.loads(self._data),list):
            keys = json.loads(self._data)
            self._object = []
            for key in keys:
                self._object.append(key)
                self._keys.append(key)
        
        elif isinstance(self._data,list):
            self._object = []
            keys = self._data
            for key in keys:
                self._object.append(key)
                self._keys.append(key)

        if not self.allowed:
            self.allowed = self._keys
            
        
        if isinstance(self._object,dict):
            for key,val in self._object.items():
                setattr(self,key,val)
        elif isinstance(self._object,list):
            for key in self._object:
                setattr(self,key,None)

    # check if is allowed key
    def is_allowed(self,key):
        return key in self.allowed
        
    # check if can add or change or delete  an attribute 
    def check(self,key):
        return True
    # check if the instance has a certain attribute
    def has_attr(self,key):
        try:self.check(key);return True
        except AttributeError:return False
        except:return False
    
    # change the object data 
    def update(self,key,val):
        self.check(key) 
        if isinstance(self._object,dict):self._object[key] = val 
        setattr(self,key,val) 
        return getattr(self,key)
    def set(self,key,val):
        self.update(key,val)

    # delete an item from the object 
    def delete(self,key):
        self.check(key) 
        if isinstance(self._object,dict):del self._object[key]
        delattr(self,key)
    # get a certain value 
    def get(self,key):
        self.check(key)
        try:return getattr(self,key)
        except: return None
        
    def has_attr(self,key):
        return hasattr(self,key)
    
    # return the fainal result for the instance -> stringfy object | dict object 
    # default is : stringfy
    def result(self,jsonFormat=True):
        if not jsonFormat:
            return self._object
        return json.dumps(self._object)

JOM = JsonObjectManager

