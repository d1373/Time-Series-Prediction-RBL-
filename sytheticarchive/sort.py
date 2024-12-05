from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['RBL']  # Replace 'your_database_name' with your actual database name
collection = db['dustbin_entries']  # Replace 'your_collection_name' with your actual collection name

# Sort documents by date in descending order
collection.find({"Dustbin_ID":1}).sort([("Date", -1), ("Time", -1)]).limit(1)
collection.find({"Dustbin_ID":2}).sort([("Date", -1), ("Time", -1)]).limit(1)
collection.find({"Dustbin_ID":3}).sort([("Date", -1), ("Time", -1)]).limit(1)
collection.find({"Dustbin_ID":4}).sort([("Date", -1), ("Time", -1)]).limit(1)
collection.find({"Dustbin_ID":5}).sort([("Date", -1), ("Time", -1)]).limit(1)
collection.find({"Dustbin_ID":6}).sort([("Date", -1), ("Time", -1)]).limit(1)
