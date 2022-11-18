from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(session_options={'autocommit': True})


class GenColumn(db.Column):

    def __init__(self, *args, **kwargs):
        """ SQLAlchemy 默认如果不指定 nullable 默认是 True.

        Source Code:
            self.primary_key = kwargs.pop('primary_key', False)
            self.nullable = kwargs.pop('nullable', not self.primary_key)

        修改规则为，如果不指定 nullable 那么默认值是 False.
        """
        if "nullable" not in kwargs:
            kwargs["nullable"] = False
        super(GenColumn, self).__init__(*args, **kwargs)


class HasIdMixin:
    id = db.Column('id', db.Integer, primary_key=True)


class OperateTimeMixin:
    createTime = GenColumn(db.DateTime, name='create_time', default=datetime.now,
                           server_default=db.func.now(), comment="创建时间")
    lastUpdateTime = GenColumn(db.DateTime, name='last_update_time', default=datetime.now,
                               server_default=db.func.now(), comment="更新时间")


class TableOperateMixin(HasIdMixin, OperateTimeMixin):
    def __init__(self, **kwargs):
        self.createTime = kwargs.pop("createTime", datetime.now())
        self.lastUpdateTime = kwargs.pop("lastUpdateTime", datetime.now())
