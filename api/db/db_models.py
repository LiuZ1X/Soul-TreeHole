#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: models.py
@time: 2025/7/21 14:25
@project: resonant-soul
@desc: 
"""
from datetime import datetime

from loguru import logger
from peewee import DateTimeField, TextField, IntegerField, Proxy, ForeignKeyField, BooleanField, SQL 
from peewee import Model

db_proxy = Proxy()


class BaseModel(Model):
    id = IntegerField(primary_key=True)
    created_at = DateTimeField(default=datetime.now)  # 创建时间
    updated_at = DateTimeField(default=datetime.now)  # 更新时间

    class Meta:
        database = db_proxy  # 延迟初始化


class User(BaseModel):
    username = TextField(unique=True)  # 用户名，唯一
    name_nick = TextField()  # 昵称
    password = TextField()  # 密码
    status = BooleanField(default=True)  # 用户状态：True=启用，False=禁用
    is_admin = BooleanField(default=False)  # 是否是管理员

    class Meta:
        table_name = 'users'


# 情绪记录模型
class Emotion(BaseModel):
    timestamp = DateTimeField(default=datetime.now)
    emotions = TextField()  # 存储List
    user_input = TextField()
    user_id = ForeignKeyField(User, backref='emotions')


# 对话记录模型
class Conversation(BaseModel):
    timestamp = DateTimeField(default=datetime.now)
    user_input = TextField()
    ai_response = TextField()
    user_id = ForeignKeyField(User, backref='conversations')


# 评估记录模型
class Assessment(BaseModel):
    timestamp = DateTimeField(default=datetime.now)
    scores = TextField()  # 存储JSON字符串
    total_score = IntegerField()
    result = TextField()
    user_id = ForeignKeyField(User, backref='assessments') 


# 树洞内容记录表
class TreeHole(BaseModel):
    # timestamp = DateTimeField(default=datetime.now) #当前的时间戳
    # content = TextField()  # 树洞内容
    # user_id = ForeignKeyField(User, backref='tree_holes')  # 外键关联用户
    # is_public = BooleanField(default=True)  # 是否公开，默认公开

    timestamp = DateTimeField(default=datetime.now) #当前的时间戳
    user_id = ForeignKeyField(User, backref='tree_holes', index=True)  # 关联注册用户（加索引）
    device_id = TextField(null=True, index=True)  # 关联匿名用户（可为空，加索引）
    content = TextField()  # 树洞内容（文本）
    image_url = TextField(null=True)  # 图片OSS地址（可为空）
    emotion_tag = TextField(
        constraints=[SQL("CHECK (emotion_tag IN ('positive', 'negative', 'neutral'))")],
        default='neutral'
    )
    create_time = DateTimeField(default=datetime.now)  # 发布时间
    is_public = BooleanField(default=True, index=True)  # 是否公开（加索引）
    is_deleted = BooleanField(default=False)  # 是否删除
    is_top = BooleanField(default=False, index=True)  # 是否置顶（热榜，加索引）
    like_count = IntegerField(default=0)  # 点赞数
    comment_count = IntegerField(default=0)  # 评论数统计

    class Meta:
        table_name = 'tree_holes'

# 互动记录表
class Interaction(BaseModel):
    treehole_id = ForeignKeyField(TreeHole, backref='interactions', index=True)  # 关联树洞内容
    user_id = ForeignKeyField(User, backref='interactions', null=True, index=True)  # 关联注册用户（可为空）
    interaction_type = TextField(
        constraints=[SQL("CHECK (interaction_type IN ('like', 'comment', 'share', 'dislike'))")],
        null=True,  # 允许为空，表示未指定互动类型
        index=True  # 添加索引以提高查询性能
    )
    anonymous_id = TextField(null=True, index=True)  # 关联匿名用户（可为空）
    comment_text = TextField(null=True)  # 评论内容（仅当 interaction_type='comment' 时有效）
    create_time = DateTimeField(default=datetime.now)

# 热榜内容表
class HotContent(BaseModel):
    treehole_id = ForeignKeyField(TreeHole, backref='hot_content')
    rank = IntegerField()  # 热榜排名
    duration = IntegerField()  # 持续时间（小时）
    create_time = DateTimeField(default=datetime.now)

class DBManager:
    def __init__(self, db_path='mindmate.db'):
        from peewee import SqliteDatabase
        # 初始化数据库连接
        self.db = SqliteDatabase(db_path)
        db_proxy.initialize(self.db)
        # 需要确保所有模型类都继承自BaseModel
        self.models = [User, Emotion, Conversation, Assessment, TreeHole, Interaction, HotContent]  # 调整顺序，确保User先创建

        # 自动创建表
        with self.db:
            self._create_tables()
            logger.info("数据库表创建成功")

    def _create_tables(self):
        """创建数据库表"""
        self.db.create_tables(self.models, safe=True)
