import pymongo

myclient=pymongo.MongoClient('mongodb://localhost:27017/')
mydb=myclient['mydatabase']
mycol=mydb['customers']


# old={'address':"Valley 345" }
# new={ "$set": { "address": "Canyon 123" } }
# mycol.update_one(old,new)
# for x in mycol.find():
#     print(x)

myquery = { "address": { "$regex": "^S" } }
newvalues = { "$set": { "name": "Minnie" } }

x = mycol.update_many(myquery, newvalues)

print(x.modified_count, "documents updated.")