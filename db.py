import pymongo
from bson.objectid import ObjectId
client = pymongo.MongoClient("mongodb+srv://piyush:piyush@idp.e06wbyq.mongodb.net/?retryWrites=true&w=majority")  # Connect to local MongoDB
db = client['test']  # Choose the database
collection = db['metadatas']  # Choose the collection

# documents = collection.find()  # Get all the documents in the collection
# for document in documents:
#     print(document)  # Print each document
document = collection.find_one({'userId': ObjectId("6640740aa82bd78dff79795a")})
print(document)

result = collection.update_one({'userId': ObjectId("6640740aa82bd78dff79795a")}, {'$set': {'bablya': 'babloo babli'}})
print(result.modified_count)
print()
print()
print()
print()
print()
document = collection.find_one({'userId': ObjectId("6640740aa82bd78dff79795a")})
print(document)