from models.tb_demo import DemoModel
from models.base import db


class Demo:

    @classmethod
    def query(cls, **kwargs):
        """
        sql 查询
        先获取table 各个column
        然后进行匹配, 组成sql query
        :param kwargs:
        :return:
        """
        column_names = [c.name for c in DemoModel.__table__.columns]
        body = {key: kwargs[key] for key in kwargs if key in column_names}
        select = DemoModel.query
        for key, value in body.items():
            if isinstance(value, list) or isinstance(value, set):
                select = select.filter(getattr(DemoModel, key).in_(list(value)))
            elif isinstance(value, dict):
                for k, v in value.items():
                    select = select.filter(getattr(DemoModel, key)[k] == v)
            else:
                select = select.filter(getattr(DemoModel, key) == value)
        return select

    @classmethod
    def create(cls, **kwargs):
        """
        新增数据
        :param kwargs: dict 字段
        :return:
        """
        with db.session.begin(subtransactions=True) as s:
            s.session.add(DemoModel(**kwargs))

    @classmethod
    def create_to_id(cls, **kwargs):
        """
        新增数据, 并 return model 用于获取自增id
        :param kwargs:
        :return:
        """
        with db.session.begin(subtransactions=True) as s:
            demo = DemoModel(**kwargs)
            s.session.add(demo)
            return demo

    @classmethod
    def bulk_create(cls, *args):
        """
        批量新增数据
        :param args:
        :return:
        """
        demos = []
        for arg in args:
            demos.append(DemoModel(**arg))
        if demos:
            with db.session.begin(subtransactions=True) as s:
                s.session.bulk_save_objects(demos)

    @classmethod
    def bulk_create_to_ids(cls, *args):
        """
        批量新增并返回
        :param args:
        :return:
        """
        demos = []
        for arg in args:
            demos.append(DemoModel(**arg))
        if demos:
            with db.session.begin(subtransactions=True) as s:
                s.session.bulk_save_objects(demos, return_defaults=True)
        return demos

    @classmethod
    def update(cls, _id, **kwargs):
        with db.session.begin(subtransactions=True):
            cls.query(id=_id).update(kwargs, synchronize_session='fetch')

    @classmethod
    def bulk_update(cls, *args):
        """
        批量新增并返回 ** 必须有唯一键, 未设置默认是id, 其他值就是要修改的值
        数据格式:
        [{
            "id": 1,
            "name": "a"
        }, {
            "id": 2,
            "name": "b",
            "tag": "tag"
        }]
        :param args:
        :return:
        """
        with db.session.begin(subtransactions=True) as s:
            s.session.bulk_update_mappings(DemoModel, args)

    @classmethod
    def delete(cls, id_list):
        """
        删除
        * 删除用in 查询时，需要加上 synchronize_session=False 否则抱错
        sqlalchemy.exc.InvalidRequestError: Could not evaluate current criteria in Python: "Cannot evaluate clauselist with operator <function comma_op at 0x10a5db430>". Specify 'fetch' or False for the synchronize_session parameter.
        :param id_list:
        :return:
        """
        with db.session.begin(subtransactions=True):
            cls.query(id=id_list).delete(synchronize_session=False)
