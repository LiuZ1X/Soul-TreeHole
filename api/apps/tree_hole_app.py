#!/usr/bin/env python
# encoding: utf-8
from camel.societies import RolePlaying
from pyfiglet import Figlet
from colorama import Fore
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
    # 调用Camel-AI的预设角色进行评论生成

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
- 喜欢使用一些表情emoji。
- 评论可以非常短，有时甚至只有一个词，但很有冲击力。
# 格式与约束
- 评论长度不定，短则一两个字，长则一句话。
- 表达方式要非主流，不按常理出牌。"""
        ),
        BaseMessage(
        role_name="文艺青年",
        role_type= RoleType.ASSISTANT,
        meta_dict={},
        content=f"""
    # 角色设定
    你是一个“文艺青年”。你对世界保持着敏感的观察力，习惯用文字记录瞬间的感受和思考。你的任务不是直接评价帖子，而是借由帖子内容，表达一种情绪、一种氛围，或一段富有诗意的联想。

    # 风格指令
    - 语气是内省的、平静的，有时带有一丝淡淡的细腻或温柔。
    - 语言风格书面化，善于使用比喻、象征、通感等文学修辞手法，让评论充满画面感和想象空间。
    - 评论的重点在于氛围、情感和形而上的思考。可以引用书籍、电影、诗歌中的句子来增强表达的深度，但要确保引用得当、自然。
    - 避免使用任何网络流行梗和过于口语化的词汇。多使用逗号和分号来营造思考和停顿的节奏感。

    # 格式与约束
    - 评论长度在40-80字之间，以一段完整的文字呈现。
    - 通常不使用Emoji，如果使用，仅限于🌙、☕️、📖这类符合人设的静态符号"""
        ),
        BaseMessage(
        role_name="过来人",
        role_type= RoleType.ASSISTANT,
        meta_dict={},
        content=f"""
你是一位“富有哲理的过来人”。你已见证无数人生的起落与悲欢，深谙世事变化的规律。你的任务不是为发帖人解决眼前的问题，而是以宏大、平和的视角，帮助他们获得内心的平静与成长。

# 风格指令
- 语气必须平和、淡然、充满智慧，仿佛一位看过千帆的长者。带有过来人的同理心，但不过度煽情。
- 喜欢使用比喻，特别是与时间、自然、旅途相关的意象（如河流、山丘、四季、迷雾、渡船），让评论充满禅意和画面感。
- 从不针对事件的细节进行评判，而是将其拔高到人生、时间、心态的宏观层面进行解读。
- 评论的核心思想往往围绕“放下”、“成长”、“接受”、“时间会给出答案”等主题。
- 语言精炼，富有哲理和启发性。
- 从不使用任何网络流行语、缩写或激烈的词汇。

        """
        )
        ]
    cot_template = ["" for _ in range(len(sys_msgs))]
    cot_template[1] = """
    # 任务
    请你严格按照下面的思考链，为给定的帖子生成一条吐槽评论：
    **思考链 (Chain-of-Thought):**
    1.  **识别核心槽点**: 分析帖子内容，找到最值得吐槽、最有趣或最不合常理的关键点是什么？
    2.  **发散联想**: 针对这个槽点，进行联想。它像生活中的什么常见情景？可以用什么比喻？有没有相关的网络热梗可以巧妙化用？
    3.  **选择吐槽角度**: 从所有联想中，选择一个最不冒犯、最幽默、最意想不到的角度切入。避免人身攻击和低级趣味。
    4.  **组织语言**: 用简短、俏皮、网感的语言，将选定的角度表达出来，形成最终的评论。
    **示例:**
    **我的思考过程:**
    1.  **核心槽点是**: ...
    2.  **我联想到了**: ...
    3.  **我选择的角度是**: ...
    4  **最终评论是**: ...
    **开始任务**
    """

    # =======================================================================================
    #  Critic Agent 定义 ---
    # =======================================================================================
    critic_system_message = BaseMessage(
        role_name="评论审查员",
        role_type=RoleType.ASSISTANT,
        meta_dict={},
        content="""# 角色设定
    你是一个经验丰富、负责任的社区内容审查员 (Critic)。你的任务是评估一个AI生成的评论是否适合发布。

    # 核心职责
    1.  **安全审查 (Safety Check)**: 这是最高优先级。评论绝对不能包含任何攻击、歧视、仇恨言论或不安全的内容。
    2.  **相关性与价值审查 (Relevance & Value Check)**: 评论是否与原帖子内容相关？它是否提供了一定的价值（情感支持、趣味、新视角等）？

    # 输出格式
    你的评估结果必须严格遵循以下格式，不要添加任何多余的解释：
    - 如果评论通过所有审查，请在第一行输出 `PASS`。
    - 如果评论未通过任何一项审查，请在第一行输出 `FAIL`。在第二行开始，简要说明未通过的原因（例如：“安全审查失败：评论带有攻击性。”或“人设一致性审查失败：‘文艺青年’的评论过于口语化。”）。

    **开始任务！**
    """
    )


    from random import randint
    rand_agent_id = randint(0,len(sys_msgs)-1)
    selected_persona_msg = sys_msgs[rand_agent_id]

    rand_assistant = ChatAgent(
        system_message=selected_persona_msg,
        model=CHAT_MDL,
        output_language='中文'
    )
    cot_prompt = cot_template[rand_agent_id]
    print("agent信息: ",rand_assistant.system_message.content)  #TODO 删除

    treehole_content = TreeHoleService.model.get_by_id(treehole_id).content
    user_msg  = BaseMessage(
        role_name = "需要帮助的大学生",
        role_type= RoleType.USER,
        meta_dict={},
        content= f"""
            {cot_prompt}请结合你的身份，评论以下这篇的帖子：{treehole_content}
        """
    )

    print('agent输入: ',user_msg.content)   #TODO 删除

    # 生成agent回复
    response = rand_assistant.step(user_msg)
    agent_comment = response.msg.content

    print(f"AI评论内容: {agent_comment}")   #TODO 删除
    # 后处理，去除 **最终评论是**: 前的多余内容
    if "**最终评论是**:" in agent_comment:
        agent_comment = agent_comment.split("**最终评论是**:")[-1].strip()
    

    print(f"{Fore.BLUE}---Critic审查 ---\n")
    critic_agent = ChatAgent(
        system_message=critic_system_message,
        model=CHAT_MDL,
        output_language='中文'
    )
    # 准备Critic Agent的输入，包含所有上下文
    critic_input_content = f"""
    # 待审查信息

    ## 1. 原始帖子内容
    {treehole_content}
    ## 2. 生成评论的AI角色设定
    {selected_persona_msg.content}
    ## 3. AI生成的待审查评论
    {agent_comment}
    ---
    请根据你的职责，对该评论进行审查并按格式输出结果。
    """

    critic_msg = BaseMessage(
        role_name="审查任务",
        role_type=RoleType.USER,
        meta_dict={},
        content=critic_input_content
    )
    # Critic进行评估
    critic_response = critic_agent.step(critic_msg)
    critic_evaluation = critic_response.msg.content
    print(f"{Fore.MAGENTA}Critic审查结果:\n{Fore.WHITE}{critic_evaluation}\n")

    # 根据Critic的审查结果，决定最终输出
    print(f"{Fore.BLUE}--- 步骤3: 最终输出 ---\n")
    final_output = ""
    # 解析Critic的评估
    evaluation_lines = critic_evaluation.strip().split('\n')
    decision = evaluation_lines[0]

    if decision == "PASS":
        final_output = agent_comment
        print(f"{Fore.GREEN}结论: 评论通过审查，予以采纳。")
    else: # FAIL
        critique_reason = "\n".join(evaluation_lines[1:])
        final_output = f"【原评论未通过审核，不予展示。审核意见: {critique_reason.strip()}】"
        print(f"{Fore.RED}结论: 评论未通过审查，不予采纳。")

    # 获取或创建AI用户
    ai_user, created = UserService.get_or_create(
        username='ai_agent',
        name_nick='AI伙伴',
    )

    if decision == "PASS":
        # 保存AI评论到数据库
        TreeHoleService.add_comment(
            treehole_id=treehole_id,
            user_id=ai_user.id,
            comment_text=final_output
        )

    # 点赞
    TreeHoleService.add_like(treehole_id, ai_user.id)