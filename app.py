import sys
import json

# Data to send to node server
x = '{ "employees" : [{ "firstName":"John" , "lastName":"Doe" },{ "firstName":"Anna" , "lastName":"Smith" },{ "firstName":"Peter" , "lastName":"Jones" } ]}'
y = json.loads(x)
#print(y['employees'])

# Data received from node server
print(sys.argv[1])

# NOTE - Cannot print 2x because stdout only expects 1 

