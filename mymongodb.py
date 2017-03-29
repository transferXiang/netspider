# -*- coding: utf-8 -*-

import pymongo
import time
import random


class MyMongoDb:
    def __init__(self, db_name, collection_name, host="localhost", port=27017):
        client = pymongo.MongoClient(host, port)
        self.db = client.get_database(db_name)
        self.collection = self.db.get_collection(collection_name)

    def insert(self, data):
        self.collection.insert(data)

    def contians(self, key):
        return self.collection.find_one(key)

    def drop_collection(self, name):
        self.db.drop_collection(name)

    def find(self,):
        return self.collection.find()

    def find_one_and_update(self, my_filter, update):
        self.collection.find_one_and_update(my_filter, {'$set': update})


if __name__ == "__main__":
    db = MyMongoDb("Test", "myCollection")
    db.drop_collection("myCollection")
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    db.insert([{"time": time_str}, {"val": random.random()}])
    if db.contians({"time": time_str}):
        print("find")
    else:
        print("not find")

    for doc in db.collection.find():
        print(doc)
