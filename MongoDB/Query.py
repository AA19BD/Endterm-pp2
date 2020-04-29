import pymongo

myclient=pymongo.MongoClient('mongodb://localhost:27017/')
mydb=myclient['mydatabase']
mycol=mydb['customers']

# myquery = { "address": {"$gt":"S" }}
myquery = { "address": {"$regex":"^S" }}
for x in mycol.find(myquery):
    print(x)

