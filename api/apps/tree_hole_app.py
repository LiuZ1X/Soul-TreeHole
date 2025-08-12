#!/usr/bin/env python
# encoding: utf-8
from camel.societies import RolePlaying

from api.apps.emotion_app import analyze_emotion, save_emotion_record, generate_emotion_chart
from api.db.services.conversation_service import ConversationService
from api.db.services.tree_hole_services import TreeHoleService
from api.db.services.user_service import UserService
from api.settings import CHAT_MDL


def create_treehole(content, user_id, is_public=True):
    """创建新的树洞"""
    # emotion_tag = analyze_emotion(content)[0]  # 简单取第一个情绪作为标签
    emotion_tag = "neutral"
    TreeHoleService.save_treehole(content=content, user_id=user_id, emotion_tag=emotion_tag, is_public=is_public)
    return {"status": "success", "message": "树洞发布成功"}


def get_treeholes(order_by='latest', limit=20):
    """获取树洞列表"""
    if order_by == 'hot':
        holes = TreeHoleService.get_hot_treeholes(limit=limit)
    else:
        holes = TreeHoleService.get_recent_treeholes(limit=limit)

    result = []
    for h in holes:
        user = UserService.get_by_id(h.user_id)
        result.append({
            "id": h.id,
            "content": h.content,
            "user_nick": user.name_nick if user else "匿名用户",
            "like_count": h.like_count,
            "comment_count": h.comment_count,
            "create_time": h.create_time.strftime("%Y-%m-%d %H:%M"),
        })
    return result


def add_comment_to_treehole(treehole_id, user_id, comment_text):
    """为树洞添加评论"""
    # 保存用户评论
    TreeHoleService.add_comment(treehole_id=treehole_id, user_id=user_id, comment_text=comment_text)

    # 触发AI自动评论
    auto_comment_treehole(treehole_id, comment_text, user_id)

    return {"status": "success", "message": "评论成功"}


def like_treehole(treehole_id, user_id):
    """点赞或取消点赞"""
    # 简单实现，实际项目中应判断是否已点赞
    TreeHoleService.add_like(treehole_id, user_id)
    return {"status": "success", "message": "点赞成功"}


def get_comments_for_treehole(treehole_id):
    """获取树洞的评论"""
    # interactions = Interaction.select().where(
    #     (Interaction.treehole_id == treehole_id) & (Interaction.interaction_type == 'comment')
    # ).order_by(Interaction.create_time.desc())

    # comments = []
    # for i in interactions:
    #     user = UserService.get_by_id(i.user_id) if i.user_id else None
    #     user_nick = "AI伙伴" if (user and user.username == 'mindmate_ai') else (user.name_nick if user else "匿名")

    #     comments.append({
    #         "user_nick": user_nick,
    #         "comment_text": i.comment_text,
    #         "create_time": i.create_time.strftime("%Y-%m-%d %H:%M"),
    #     })

    interactions = TreeHoleService.get_interactions(treehole_id)
    comments = []
    print("\nget_comments_for_treehole success!!!\n")
    return comments


def auto_comment_treehole(treehole_id, comment_text, user_id=None, anonymous_id=None):
    """自动评论树洞内容"""
    # 这里可以调用Camel-AI的预设角色进行评论生成、自动点赞等功能

    # 1. 创建角色扮演会话
    task_prompt = "你是一个温暖、善解人意的伙伴，请用积极、鼓励的语言对用户的树洞内容进行评论。"
    role_play_session = RolePlaying(
        assistant_role_name="心灵伙伴",
        assistant_agent_kwargs=dict(model=CHAT_MDL),
        user_role_name="倾诉者",
        user_agent_kwargs=dict(model=CHAT_MDL),
        task_prompt=task_prompt,
        with_task_specify=False,
    )

    # 2. 初始化对话
    treehole_content = TreeHoleService.model.get_by_id(treehole_id).content
    input_msg = role_play_session.init_chat(
        f"这是我刚才发布的树洞内容：'{treehole_content}'。这是刚刚收到的评论：'{comment_text}'。请你作为我的心灵伙伴，给我一些温暖的回复。"
    )

    # 3. 生成AI回复
    assistant_response, _ = role_play_session.step(input_msg)
    ai_comment = assistant_response.msg.content

    # 4. 获取或创建AI用户 TODO UserService中暂时没有这个功能
    ai_user, created = UserService.get_or_create(
        username='mindmate_ai',
        defaults={'name_nick': 'AI伙伴', 'password': 'password'}
    )

    # 5. 保存AI评论到数据库
    TreeHoleService.add_comment(
        treehole_id=treehole_id,
        user_id=ai_user.id,
        comment_text=ai_comment
    )

# #这里使用的Camel-AI进行单/多agent的智能回复行为


# def auto_comment_treehole(treehole_id, comment_text, user_id=None, anonymous_id=None):
#     """自动评论树洞内容"""
#     # 这里可以调用Camel-AI的预设角色进行评论生成、自动点赞等功能
    
#     # 创建角色会话 TODO

#     # 初始化提示词 TODO

#     # 调用大模型进行对话 TODO

#     # 保存树洞内容到树洞数据库
    

# class CounselorAgent:
#     def respond(self, user_input):
#         # 调用Camel-AI的预设心理咨询师角色
#         return ai_engine.generate_response("counselor", user_input)

# class ListenerAgent:
#     def respond(self, user_input):
#         # 简单的倾听者角色
#         return f"我能感受到你的{emotion_analysis(user_input)}，请继续说。"