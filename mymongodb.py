# -*- coding: utf-8 -*-

import pymongo
import time
import random


class MyMongoDb:
    def __init__(self, db_name, cellection_name, host="localhost", port=27017):
        client = pymongo.MongoClient(host, port)
        self.db = client.get_database(db_name)
        self.collection = self.db.get_collection(cellection_name)

    def insert(self, data):
        self.collection.insert(data)

    def contians(self, key):
        return self.collection.find_one(key)

    def drop_collection(self, name):
        self.db.drop_collection(name)

    def find(self,):
        return self.collection.find()

    def find_one_and_update(self, filter, update):
        self.collection.find_one_and_update(filter, {'$set': update})


if __name__ == "__main__":
    db = MyMongoDb("Test", "myCollection")
    db.drop_collection("myCollection")
    db.insert([{"time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))},
               {"val": random.random()}])
    if db.contians({"time": time.time()}):
        print "find"
    else:
        print "not find"

    for doc in db.collection.find():
        if doc.has_key('time'):
            print doc['time']