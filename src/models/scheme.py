import uuid

from src.common.database import Database

class Scheme(object):

    def __init__(self, scheme_group_name, scheme_name, work_group_name, work_type, _id=None):

        self.scheme_group_name = scheme_group_name
        self.scheme_name = scheme_name
        self.work_group_name = work_group_name
        self.work_type = work_type
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):

        Database.insert(collection='schemes', data=self.json())

    @classmethod
    def update_scheme(cls, _id, scheme_group_name, scheme_name, work_group_name, work_type):
        Database.update_scheme(collection='schemes', query={'_id': _id}, scheme_group_name=scheme_group_name,

                              scheme_name=scheme_name, work_group_name=work_group_name,

                              work_type=work_type)

    def json(self):

        return {

            'scheme_group_name': self.scheme_group_name,

            'scheme_name': self.scheme_name,

            'work_group_name': self.work_group_name,

            'work_type': self.work_type,

            '_id': self._id,

        }




