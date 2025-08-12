#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime, timedelta

from api.db.db_models import TreeHole
from peewee import fn

class TreeHoleService:
    model = TreeHole

    @classmethod
    def add_comment(cls, treehole_id, user_id=None, anonymous_id=None, comment_text=None):
        """新增评论并同步更新评论数"""
        from api.db.db_models import Interaction
        # 创建评论互动
        Interaction.create(
            treehole_id=treehole_id,
            user_id=user_id,
            anonymous_id=anonymous_id,
            comment_text=comment_text,
            interaction_type='comment'
        )
        # 更新评论数
        query = cls.model.update(comment_count=cls.model.comment_count + 1).where(cls.model.id == treehole_id)
        query.execute()
        return True

    @classmethod
    def delete_comment(cls, interaction_id):
        """删除评论并同步更新评论数"""
        from api.db.db_models import Interaction
        interaction = Interaction.get_or_none(Interaction.id == interaction_id)
        if interaction and interaction.interaction_type == 'comment':
            treehole_id = interaction.treehole_id.id
            interaction.delete_instance()
            # 更新评论数
            query = cls.model.update(comment_count=cls.model.comment_count - 1).where(cls.model.id == treehole_id)
            query.execute()
            return True
        return False

    @classmethod
    def add_like(cls, treehole_id, user_id=None, anonymous_id=None):
        """新增点赞并同步更新点赞数"""
        from api.db.db_models import Interaction
        Interaction.create(
            treehole_id=treehole_id,
            user_id=user_id,
            anonymous_id=anonymous_id,
            interaction_type='like'
        )
        query = cls.model.update(like_count=cls.model.like_count + 1).where(cls.model.id == treehole_id)
        query.execute()
        return True

    @classmethod
    def delete_like(cls, interaction_id):
        """删除点赞并同步更新点赞数"""
        from api.db.db_models import Interaction
        interaction = Interaction.get_or_none(Interaction.id == interaction_id)
        if interaction and interaction.interaction_type == 'like':
            treehole_id = interaction.treehole_id.id
            interaction.delete_instance()
            query = cls.model.update(like_count=cls.model.like_count - 1).where(cls.model.id == treehole_id)
            query.execute()
            return True
        return False

    @classmethod
    def save_treehole(cls, content, user_id, device_id=None, image_url=None, emotion_tag='neutral', is_public=True):
        """保存树洞内容"""
        cls.model.create(
            content=content,
            user_id=user_id,
            device_id=device_id,
            image_url=image_url,
            emotion_tag=emotion_tag,
            is_public=is_public
        )

    @classmethod
    def soft_delete_treehole(cls, treehole_id):
        """软删除树洞内容(设置is_deleted为True)"""
        query = cls.model.update(is_deleted=True).where(cls.model.id == treehole_id)
        return query.execute()  # 返回受影响的行数

    @classmethod
    def get_recent_treeholes(cls, limit=10):
        """获取最近(时间倒序)的树洞内容"""
        query = (cls.model
                 .select()
                 .where(cls.model.is_deleted == False)
                 .order_by(cls.model.create_time.desc())
                 .limit(limit))
        # return [(t.id, t.content, t.image_url, t.emotion_tag, t.create_time.strftime("%Y-%m-%d %H:%M:%S"))
        #         for t in query]
        return [{'user_id': t.user_id, 'content': t.content, 'image_url': t.image_url, 'emotion_tag': t.emotion_tag, 'create_time': t.create_time.strftime("%Y-%m-%d %H:%M:%S")}
                for t in query]
    
    @classmethod
    def get_hot_treeholes(cls, limit=10):
        """获取热榜树洞内容（按置顶和点赞数倒序）"""
        query = (cls.model
                 .select()
                 .where((cls.model.is_deleted == False) & (cls.model.is_public == True))
                 .order_by(cls.model.is_top.desc(), cls.model.like_count.desc(), cls.model.create_time.desc())
                 .limit(limit))
        # return [(t.id, t.content, t.image_url, t.emotion_tag, t.like_count, t.is_top, t.create_time.strftime("%Y-%m-%d %H:%M:%S"))
        #         for t in query]
        return [{'user_id': t.user_id, 'content': t.content, 'image_url': t.image_url, 'emotion_tag': t.emotion_tag, 'create_time': t.create_time.strftime("%Y-%m-%d %H:%M:%S")}
                for t in query]

    @classmethod
    def get_interactions(cls, treehole_id):
        """获取树洞的互动记录"""
        query = cls.model.select().where(cls.model.id == treehole_id)
        if query.exists():
            return query[0].interactions
        return []
    