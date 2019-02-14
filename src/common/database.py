import pymongo
import os


class Database(object):

    # URI = os.environ['MONGODB_URI']
    # DATABASE = None
    #
    # @staticmethod
    #
    # def initialize():
    #
    #     client = pymongo.MongoClient(Database.URI)
    #     Database.DATABASE = client['heroku_thg5d5x0']

    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
         client = pymongo.MongoClient(Database.URI)
         Database.DATABASE = client['Dindugul']

    @staticmethod
    def insert(collection, data):

        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):

        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):

        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update_stage(collection, query, stage_name, stage_order_id, work_id, start_date, end_date, amount, total_stages,
                     user_id, user_name, stage_status):

        return Database.DATABASE[collection].update_one(query, {'$set': {'stage_name': stage_name,

                                                                         'stage_order_id': stage_order_id,

                                                                         'work_id': work_id,

                                                                         'start_date': start_date,

                                                                         'end_date': end_date,

                                                                         'amount': amount,

                                                                         'stage_status': stage_status,

                                                                         'total_stages': total_stages,

                                                                         'user_id' : user_id,

                                                                         'user_name' : user_name }}, True)

    @staticmethod
    def update_work(collection, query, amount, start_date, end_date, block, total_stages, panchayat, habitation,
                    user_id, user_name, work_status, work_name, amount_spent, scheme_group_name, scheme_name, work_group_name, work_type):
        return Database.DATABASE[collection].update_one(query, {'$set': {'amount': amount,
                                                                         'start_date': start_date,
                                                                         'end_date': end_date,
                                                                         'block': block,
                                                                         'panchayat': panchayat,
                                                                         'habitation': habitation,
                                                                         'total_stages': total_stages,
                                                                         'amount_spent': amount_spent,
                                                                         'work_status' : work_status,
                                                                         'user_id' : user_id,
                                                                         'user_name' : user_name,
                                                                         'work_name' : work_name,
                                                                         'scheme_group_name': scheme_group_name,
                                                                         'scheme_name': scheme_name,
                                                                         'work_group_name': work_group_name,
                                                                         'work_type': work_type}}, True)

    @staticmethod
    def update_scheme(collection, query, scheme_group_name, scheme_name, work_group_name, work_type):

         return Database.DATABASE[collection].update_one(query, {'$set': {'scheme_name': scheme_name,

                                                                          'scheme_group_name': scheme_group_name,

                                                                          'work_group_name': work_group_name,

                                                                          'work_type': work_type}}, True)

    @staticmethod
    def update_current_stage(collection, query, stage_name, stage_order_id):

         return Database.DATABASE[collection].update_one(query, {'$set': {'stage_name': stage_name,
                                                                          'stage_order_id': int(stage_order_id)+1}}, True)


    @staticmethod
    def update_work_name(collection, query, work_name):
        return Database.DATABASE[collection].update_one(query, {'$set': {'work_name': work_name}}, True)

    @staticmethod
    def delete_from_mongo(collection, query):

        print(query)

        Database.DATABASE[collection].remove(query)

