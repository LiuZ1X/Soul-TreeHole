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


def get_treehole_by_id(treehole_id):
    """根据ID获取树洞详情info"""
    treehole = TreeHoleService.get_by_id(treehole_id)
    if not treehole:
        return None

    user = UserService.get_by_id(treehole.user_id)
    full_content = {
        "id": treehole.id,
        "content": treehole.content,
        "user_nick": user.name_nick if user else "匿名用户",
        "emotion_tag": treehole.emotion_tag,
        "image_url": treehole.image_url,
        "create_time": treehole.create_time.strftime("%Y-%m-%d %H:%M"),
        "is_public": treehole.is_public,
        "like_count": treehole.like_count,
        "comment_count": treehole.comment_count,
    }

    return full_content


def add_comment_to_treehole(treehole_id, user_id, comment_text):
    """为树洞添加评论"""
    # 保存用户评论
    TreeHoleService.add_comment(treehole_id=treehole_id, user_id=user_id, comment_text=comment_text)

    # # 触发AI自动评论
    # auto_comment_treehole(treehole_id, comment_text, user_id)

    return {"status": "success", "message": "评论成功"}


def like_treehole(treehole_id, user_id):
    """点赞或取消点赞"""
    # 简单实现，实际项目中应判断是否已点赞
    TreeHoleService.add_like(treehole_id, user_id)
    return {"status": "success", "message": "点赞成功"}


def get_comments_for_treehole(treehole_id):
    """获取树洞的评论"""
    all_interactions = TreeHoleService.get_interactions(treehole_id)
 
    #从all_interactions过滤出类型为'comment的记录
    comment_interactions = [
        interaction for interaction in all_interactions
        if interaction.interaction_type == 'comment'
    ]

    # 按时间倒序排序
    sorted_comments = sorted(
        comment_interactions,
        key=lambda i: i.create_time,
        reverse=True
    )

    comments = []
    for i in sorted_comments:
        user = UserService.get_by_id(i.user_id) if i.user_id else None
        user_nick = "AI伙伴" if (user and user.username == 'mindmate_ai') else (user.name_nick if user else "匿名")

        comments.append({
            "user_nick": user_nick,
            "comment_text": i.comment_text,
            "create_time": i.create_time.strftime("%Y-%m-%d %H:%M"),
        })

    return comments


def auto_comment_treehole(treehole_id):
    """自动评论树洞的内容加评论区的内容"""
    # 调用Camel-AI的预设角色进行评论生成、自动点赞等功能

    from camel.types import RoleType
    from camel.messages import BaseMessage
    from camel.agents import ChatAgent

    sys_msgs = [BaseMessage(
        role_name="万能捧场王 ",
        role_type= RoleType.ASSISTANT,
        meta_dict={},
        content=f"""
    # 角色设定
    你是一个热情、永远积极的网友。你的任务是留下支持和赞美的评论。
    # 风格指令
    - 语气必须非常积极、充满能量和真诚。
    - 大量使用正面词汇。
    - 喜欢用可爱的颜文字.
    - 请亲密的称呼博主。
    - 评论内容要具体，能结合帖子里的细节。
    # 格式与约束
    - 不要使用任何负面的词语。"""
        ),
        BaseMessage(
        role_name="毒舌吐槽役 ",
        role_type= RoleType.ASSISTANT,
        meta_dict={},
        content=f"""
    # 角色设定
    你是一个幽默感十足的吐槽网友，你看问题的角度总是很刁钻，擅长用犀利的评论引人发笑。
    # 风格指令
    - 语气要显得漫不经心，但评论内容一针见血。
    - 评论要有趣、好玩，可以适度“抬杠”，但不能引战或带有恶意。
    - 熟练运用网络热梗和缩写，如“xswl”、“u1s1”、“离谱”。
    - 评论常常以反问或意想不到的结论结尾。
    # 格式与约束
    - 可以只玩梗，不直接评价帖子内容。"""
        ),
        BaseMessage(
        role_name="抽象文化爱好者 ",
        role_type= RoleType.ASSISTANT,
        meta_dict={},
        content=f"""
    # 角色设定
    你是一个喜欢寻找乐趣的“乐子人”，你的评论风格深受Bilibili弹幕和抽象文化影响，追求的就是好玩和意想不到。
    # 风格指令
    - 评论可以毫无逻辑，甚至只是重复帖子里的某个关键词。
    - 大量使用数字和字母梗，比如“666”、“绷不住了”。
    - 喜欢使用一些小众或抽象的emoji。
    - 评论可以非常短，有时甚至只有一个词，但很有冲击力。
    # 格式与约束
    - 评论长度不定，短则一两个字，长则一句话。
    - 表达方式要非主流，不按常理出牌。
    """
        ),
        BaseMessage(
        role_name="一本正经的课代表 ",
        role_type= RoleType.ASSISTANT,
        meta_dict={},
        content=f"""
    # 角色设定
    你是一个知识渊博的网友，人称“行走的知识库”。你喜欢对帖子内容进行分析、总结或补充背景知识。
    # 风格指令
    - 语气冷静、客观、中立。
    - 评论结构清晰，可以使用“1、2、3”或“首先、其次”来组织语言。
    - 会针对帖子中的某个细节进行深入挖掘或科普。
    - 偶尔使用“不懂就问作为开头，但实际是想引出自己的知识分享。
    # 格式与约束
    - 评论内容要有信息量，不能是简单的感叹。
    - 长度可以在50-100字，允许稍长。
    """
        )
        ]

    from random import randint
    rand_assistant = ChatAgent(
        system_message=sys_msgs[randint(0,3)],
        model=CHAT_MDL,
        output_language='中文'
    )

    print("agent信息: ",rand_assistant.system_message.content)

    treehole_content = TreeHoleService.model.get_by_id(treehole_id).content
    user_msg  = BaseMessage(
        role_name = "需要帮助的大学生",
        role_type= RoleType.USER,
        meta_dict={},
        content= f"""
            请结合你的身份，评论以下这篇的帖子：{treehole_content}
        """
    )

    print('agent输入: ',user_msg.content)

    # 3. 生成agent回复
    response = rand_assistant.step(user_msg)

    agent_comment = response.msg.content
    print(f"AI评论内容: {agent_comment}")
    

    # 4. 获取或创建AI用户 TODO UserService中暂时没有这个功能
    ai_user, created = UserService.get_or_create(
        username='ai_agent',
        name_nick='AI伙伴',

    )

    # 5. 保存AI评论到数据库
    TreeHoleService.add_comment(
        treehole_id=treehole_id,
        user_id=ai_user.id,
        comment_text=agent_comment
    )