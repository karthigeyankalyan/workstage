import uuid

from datetime import datetime

from src.common.database import Database


class Stage(object):



    def __init__(self, stage_name, stage_order_id, amount, user_name, user_id, stage_status= 'Open', work_id=None, start_date=None,

                 end_date=None, total_stages=None, _id=None, work_name=None):



        if start_date:

            self.start_date = datetime.combine(datetime.strptime(start_date, '%Y-%m-%d').date(),

                                                 datetime.now().time())

        else:

            self.start_date = None



        if end_date:

            self.end_date = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d').date(),

                                                datetime.now().time())

        else:

            self.end_date = None

        self.stage_name = stage_name

        self.stage_order_id = stage_order_id

        self.work_id = work_id

        self.amount = amount

        self.total_stages = total_stages

        self.stage_status = stage_status

        self.work_name = work_name

        self.user_id = user_id

        self.user_name = user_name

        self._id = uuid.uuid4().hex if _id is None else _id


    def save_to_mongo(self):

        Database.insert(collection='stages', data=self.json())



    @classmethod

    def update_stage(cls, _id, stage_name, stage_order_id, work_id, start_date, end_date, amount, total_stages,
                     user_id, user_name, stage_status):

        Database.update_stage(collection='stages', query={'_id': _id}, stage_name=stage_name,

                                stage_order_id=stage_order_id, work_id=work_id,

                                start_date=start_date, end_date=end_date, amount=amount, user_id=user_id,

                                user_name=user_name, total_stages=total_stages, stage_status=stage_status)

    @classmethod
    def update_work_name(cls, work_name ,work_id):

        Database.update_work_name(collection='stages', query={'work_id': work_id}, work_name=work_name)

    def json(self):

        return {

            'stage_name': self.stage_name,

            'stage_order_id': self.stage_order_id,

            'amount': self.amount,

            'start_date': self.start_date,

            'end_date': self.end_date,

            'total_stages': self.total_stages,

            'work_id': self.work_id,

            'work_name': self.work_name,

            'stage_status': self.stage_status,

            'user_id': self.user_id,

            'user_name': self.user_name,

            '_id': self._id,

        }



    @classmethod

    def from_mongo(cls, _id):

        Intent = Database.find_one(collection='stages', query={'_id': _id})

        return cls(**Intent)

    @classmethod
    def deletefrom_mongo(cls, _id):

        Database.delete_from_mongo(collection='stages', query={'_id': _id})

    @classmethod

    def find_by_district(cls, blocks):

        intent = Database.find(collection='accounts', query={'blocks': blocks})

        return [cls(**inten) for inten in intent]