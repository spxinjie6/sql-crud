from models.base import (
    db,
    TableOperateMixin,
    GenColumn)


class DemoModel(db.Model, TableOperateMixin):
    """
CREATE TABLE `tb_demo` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `name` varchar(100) NOT NULL DEFAULT '' COMMENT '名称',
  `tag` varchar(100) NOT NULL DEFAULT '' COMMENT '标签',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='demo';
    """
    __tablename__ = "tb_demo"

    name = GenColumn(db.String(100), name="name", default="", comment="名称")
    tag = GenColumn(db.String(100), name="tag", default="", comment="标签")

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.tag = kwargs.get("tag")
        super().__init__()
