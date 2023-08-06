import json
class JsonObjectManager:
    # allowed attributes is a list contains wich  attributes you allowed to be added in this object
    # the Class will not append any other attribute that is out of this list 
    # default: all the keys in your data object 
    # you can not disallow any key that is in your data object 
    allowed = []
    def __init__(self,data,allowed=[]):
        # object data -> str(Json Object) | list(Any) | dict(key&value)
        self.data = data
        # instance controler -> dict : handled by the instance 
        self.object = None
        # desc in the top ^ 
        self.allowed = allowed
        # instance keys 
        self.keys = []
        # handle data object 
        self.handle_data()

    # handle data object 
    def handle_data(self):
        if isinstance(self.data,str) and isinstance(json.loads(self.data),dict):
            self.object = {}
            keys = json.loads(self.data)
            for key,val in keys.items():
                self.object[key] = val
                self.keys.append(key)

        elif  isinstance(self.data,dict):
            self.object = {}
            keys = self.data
            for key,val in keys.items():
                self.object[key] = val
                self.keys.append(key)


        elif isinstance(self.data,str) and isinstance(json.loads(self.data),list):
            keys = json.loads(self.data)
            self.object = []
            for key in keys:
                self.object.append(key)
                self.keys.append(key)
        
        elif isinstance(self.data,list):
            self.object = []
            keys = self.data
            for key in keys:
                self.object.append(key)
                self.keys.append(key)

        if not self.allowed:
            self.allowed = self.keys

    # check if is allowed key
    def is_allowed(self,key):
        return key in self.allowed
        
    # check if can add or change or delete  an attribute 
    def check(self,key):
        if not self.is_allowed(key): raise AttributeError(' Object does not have a key named %s '%(key))
    # check if the instance has a certain attribute
    def has_attr(self,key):
        try:self.check(key);return True
        except AttributeError:return False
        except:return False
    
    # change the object data 
    def change_val(self,key,val):
        self.check(key);self.object[key] = val ; setattr(self,key,val) ;return getattr(self,key)
    # delete an item from the object 
    def del_item(self,key):
        self.check(key) ;del self.object[key] ;delattr(self,key)
    
    # get a certain value 
    def get_val(self,key):
        self.check(key) ; return getattr(self,key)
    
    # return the fainal result for the instance -> stringfy object | dict object 
    # default is : stringfy
    def result(self,type='json'):
        if type != 'json':
            return self.object
        return json.dumps(self.object)

JOM = JsonObjectManager

