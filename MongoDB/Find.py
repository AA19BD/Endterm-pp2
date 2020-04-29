import pymongo

myclient=pymongo.MongoClient('mongodb://localhost:27017/')
mydb=myclient['mydatabase']
mycol=mydb['customers']

# x=mycol.find_one()
# print(x)

# for x in mycol.find():
#     print(x)

for x in mycol.find({},{'name':1,'address':1}):
    print(x)
# for x in mycol.find({},{'name':1}):
#    print(x)
