import uuid

from datetime import datetime

from src.common.database import Database

class Work(object):

    def __init__(self, amount, work_name, user_id, user_name, block, scheme_group_name, scheme_name, work_group_name, work_type,
                    work_status='Open', amount_spent=None, total_stages=None,
                    start_date=None, end_date=None, work_id=None):



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



        self.block = block

        self.amount = amount

        self.total_stages = total_stages

        self.user_id = user_id

        self.user_name = user_name

        self.work_status = work_status

        self.work_name = work_name

        self.scheme_group_name = scheme_group_name

        self.scheme_name = scheme_name

        self.work_group_name = work_group_name

        self.work_type = work_type

        self.amount_spent = amount_spent

        self.work_id = uuid.uuid4().hex if work_id is None else work_id


    def save_to_mongo(self):

        Database.insert(collection='works', data=self.json())

    @classmethod

    def update_work(cls, work_name, work_id, block, start_date, end_date, amount, total_stages, amount_spent,
                    scheme_group_name, scheme_name, work_group_name, work_type,
                     user_id, user_name, work_status,):

        Database.update_work(collection='works', query={'work_id': work_id}, block=block,

                                amount_spent = amount_spent, scheme_group_name=scheme_group_name, scheme_name = scheme_name,

                                work_group_name=work_group_name, work_type=work_type,

                                start_date=start_date, end_date=end_date, amount=amount, user_id=user_id,

                                user_name=user_name, total_stages=total_stages, work_status=work_status, work_name = work_name)

    @classmethod
    def update_current_stage(cls, stage_name, stage_order_id, work_id):

        Database.update_current_stage(collection='works', query={'work_id': work_id}, stage_name=stage_name,

                                                                             stage_order_id=stage_order_id)

    def json(self):

        return {

            'block': self.block,

            'amount': self.amount,

            'start_date': self.start_date,

            'end_date': self.end_date,

            'total_stages': self.total_stages,

            'user_id': self.user_id,

            'user_name': self.user_name,

            'work_id': self.work_id,

            'work_status': self.work_status,

            'work_name' : self.work_name,

            'amount_spent': self.amount_spent,

            'scheme_group_name': self.scheme_group_name,

            'scheme_name': self.scheme_name,

            'work_group_name': self.work_group_name,

            'work_type': self.work_type,
        }



    @classmethod

    def from_mongo(cls, work_id):

        Intent = Database.find_one(collection='works', query={'work_id': work_id})

        return cls(**Intent)

    @classmethod

    def find_by_district(cls, blocks):

        intent = Database.find(collection='works', query={'blocks': blocks})

        return [cls(**inten) for inten in intent]