# JOM Django JsonField simple manager

JOM Object helps you to handle JsonField in django frame work 
so that you can (delete | edit | add ) values and gets the result from the function
result() 
you can get two types of results (str -> json object | dict -> python object)

> example 

```python

from jom import JOM 
# or you can import it as JsonObjectManager

# asign the object you want to handle 
# json format 
data = "{'name':'Hussein Naim ','website':'https://iamhusseinnaim.github.io','age':22}"

# allowed fields to deal with 
allowed = ['name','website','age']
# create the instance 
instance = JSOM(data,allowed=allowed)
# delete a certain item
instance.del_item("age")
# holding the result 
result = instance.result()
# print out the result
print(result)

# output: default = return as json | str 
# "{'name':"Hussein Naim ","website":"https://iamhusseinnaim.github.io"}


```