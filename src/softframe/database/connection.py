
from pymongo import MongoClient
from bson.objectid import ObjectId


class DatabaseConnector(object):

    def __init__(self, conn=None, host=None, port=None):
        self.db = None
        self.client = None
        self.collection = None

        if conn is None:
            try:
                if host is None and port is None:
                    self.client = MongoClient()
                else:
                    self.client = MongoClient(host=host, port=port)
            except Exception as e:
                print(repr(e))
        else:
            if isinstance(conn, type(MongoClient())):
                self.client = conn

        self.db = self.client["test_database"]

    def set_db(self, name):
        if name is not None and name is not "":
            self.db = self.client[name]

    def get_db(self):
        if self.db is None:
            print("Database is None.")
            return None

        return self.db

    def set_collection(self, name):
        if name is not None and name is not "":
            self.collection = self.db[name]

    def get_collection(self):
        if self.collection is None:
            print("Collection is None.")
            return None

        return self.collection

    def get_item(self, id_=None):
        if self.collection is None:
            print("Collection and Database should be set.")
            return None

        else:
            if id_ is None:
                return self.collection.find_one()
            else:
                return self.collection.find_one({'_id': ObjectId(id)})

    def get_items_by_field(self, field, value):
        if self.collection is None:
            print("Collection and Database should be set.")
            return None

        else:
            if "_id" in field:
                return [x for x in self.collection.find({field: ObjectId(value)})]

            return [x for x in self.collection.find({field: value})]

    def get_all_items(self):
        """ Return a list with every json element from the collection. """
        if self.collection is not None:
            result = self.collection.find()
            return [x for x in result]

    def insert_item(self, item):
        try:
            id = self.collection.insert_one(item).inserted_id
            return id
        except Exception as e:
            print(repr(e))
            return None

    def bulk_insert_items(self, items_list):
        try:
            result = self.collection.insert_many(items_list)
            return result.inserted_ids
        except Exception as e:
            print(repr(e))
            return None

    def delete_by_id(self, id):
        try:
            result = self.collection.delete_one({"_id": ObjectId(id)})
            return result.deleted_count
        except Exception as e:
            print(repr(e))
            return None

    def close_connection(self):
        if self.client is not None:
            self.client.close()


def main():
    conn = DatabaseConnector()

    conn.set_collection("documents")
    #posts = {"author": "Mike", "text": "My first blog post!", "tags": ["mongodb", "python", "pymongo"], "date": datetime.datetime.utcnow()}#,
    #       {"author": "Tyson", "text": "Boxing is life.", "tags": ["boxe", "fighting"], "date": datetime.datetime.utcnow()},
    #        {"author": "Charlotte", "text": "Go Hornets", "tags": ["basquetball", "nba"], "date": datetime.datetime.utcnow()}]
    #res_id = conn.bulk_insert_items(posts)
    #res_id = conn.insert_item(posts)

    print(conn.get_all_items())
    #print(conn.delete_by_id(res_id))
    #print(conn.get_all_items())

    conn.close_connection()

if __name__ == "__main__":
    main()
