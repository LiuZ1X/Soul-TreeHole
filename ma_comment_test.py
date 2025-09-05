from pyfiglet import Figlet
from colorama import Fore

from camel.utils import print_text_animated
from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import RoleType
import random

# --- 模型和数据设置 (与原代码相同) ---
CHAT_MDL = ModelFactory.create(
    model_platform=ModelPlatformType.OLLAMA,
    model_type="qwen2.5:7b",
    model_config_dict={"temperature": 0.7, 'max_tokens': 4096},
)

text_list = ["六点半的闹钟响了三次才爬起来，窗外灰蒙蒙的。冲去教室发现教授请假了，群里通知九点才更新...空着肚子在冷风里站半小时，咖啡洒了一书包。这学期第4次了，我真的会恨早八。",
"凌晨两点给PPT收尾，发现队友交来的数据全是错的。微信群里@所有人，三个装死一个说‘明天再改吧’。想骂人又怕被说斤斤计较，最后自己重做三小时。明明小组作业，为什么永远只有我在焦虑？",
"今天在食堂刷卡时余额不足，后面排队的男生直接帮我付了钱。我慌张道谢，他说‘上次我饭卡没钱你也帮过我呀’...完全想不起他是谁。原来陌生人之间也会像洋葱一样，剥开冷淡的外皮藏着暖意。",
"连续三周在靠窗座位遇到那个读《百年孤独》的女生。今天她突然放了一盒草莓在我桌上，纸条写着‘看你总啃面包’。我耳朵发烫埋头道谢，她却像风一样走了。现在对着草莓傻笑，书一页没翻。",
"收到dream公司拒信时正在教学楼走廊，电话那头说‘你很优秀但经验不足’。强撑着笑说谢谢，转身冲进厕所隔间哭得发抖。出来时发现下雨了，没带伞。雨水打湿简历上‘精通Python’那行字，墨迹晕成一团乌云。",
"她们聊综艺时我插了句‘那个主持人学历造假’，空气突然安静。有人冷笑：‘学霸就是爱扫兴。’ 我缩回床帘里刷手机，光刺得眼睛疼。其实我只是...想加入聊天啊。",
"取快递时机器故障，后面男生主动帮我抬箱子。闲聊发现是同乡，还都喜欢拼图。分开时他喊‘下次拼图交换啊！’ 抱着箱子蹦跳回宿舍，连破纸箱刮腿都觉得开心。原来快乐是颗跳跳糖，猝不及防在舌尖炸开。",
"800米最后半圈肺像烧起来，耳边全是粗重喘息。突然听见跑道边有人喊我名字加油，是辩论队打过对手的姑娘。咬牙冲刺时眼泪混着汗往下淌——被看见狼狈，却也意外被托住了。",
"记账APP弹出本月超支警告。看看账单：教材打印98元，考研网课199，给奶奶寄膏药165...犹豫很久删掉购物车的裙子。妈妈打电话问‘钱够用吗’，我咽下食堂免费的汤说‘够的，还有剩呢’。",
"从实验室出来已近午夜，耳机里放着《你曾是少年》。抬头看见路灯下飞蛾绕着光打转，那么固执地扑向虚幻的热源。突然懂了导师说的‘科研就是做一只快乐的蠢蛾子’——明知真理不可及，仍为刹那靠近欣喜。"
]

# 随机选择一个帖子进行评论
user_input = random.choice(text_list)

# --- 角色Agent定义 (与原代码相同) ---
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
- 喜欢使用比喻，特别是与时间、自然、旅途相关的意象（如河流、山丘、四季、迷霧、渡船），让评论充满禅意和画面感。
- 从不针对事件的细节进行评判，而是将其拔高到人生、时间、心态的宏观层面进行解读。
- 评论的核心思想往往围绕“放下”、“成长”、“接受”、“时间会给出答案”等主题。
- 语言精炼，富有哲理和启发性。
- 从不使用任何网络流行语、缩写或激烈的词汇。

    """
    )
    ]

# --- CoT模板 (与原代码相同) ---
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
# --- 新增: Critic Agent 定义 ---
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

# =======================================================================================
# --- 主流程修改: 引入生成-审核机制 ---
# =======================================================================================

# 1. 随机选择一个角色Agent进行评论生成
rand_agent_id = random.randint(0, len(sys_msgs) - 1)
selected_persona_msg = sys_msgs[rand_agent_id]

# 初始化生成评论的Agent
assistant_agent = ChatAgent(
    system_message=selected_persona_msg,
    model=CHAT_MDL,
    output_language='中文'
)
print("="*50)
print(f"{Fore.CYAN}被评论的帖子内容:\n{Fore.WHITE}{user_input}")
print(f"\n{Fore.CYAN}随机选定的评论角色: {Fore.YELLOW}{selected_persona_msg.role_name.strip()}")
print("="*50)

# 准备生成Agent的输入
cot_prompt = cot_template[rand_agent_id]
user_msg_for_assistant = BaseMessage(
    role_name="需要帮助的大学生",
    role_type=RoleType.USER,
    meta_dict={},
    content=f"""{cot_prompt} 请结合你的身份，评论以下这篇的帖子：{user_input}"""
)

# 生成初步评论
response = assistant_agent.step(user_msg_for_assistant)
initial_comment = response.msg.content

# 对CoT输出进行后处理
if "**最终评论是**:" in initial_comment:
    initial_comment = initial_comment.split("**最终评论是**:")[-1].strip()

print(f"\n{Fore.BLUE}--- 步骤1: 初步生成 ---\n{Fore.WHITE}{initial_comment}\n")


# 2. Critic Agent介入，进行审核
print(f"{Fore.BLUE}--- 步骤2: Critic审查 ---\n")
critic_agent = ChatAgent(
    system_message=critic_system_message,
    model=CHAT_MDL,
    output_language='中文'
)

# 准备Critic Agent的输入，包含所有上下文
critic_input_content = f"""
# 待审查信息

## 1. 原始帖子内容
{user_input}

## 2. 生成评论的AI角色设定
{selected_persona_msg.content}

## 3. AI生成的待审查评论
{initial_comment}

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


# 3. 根据Critic的审查结果，决定最终输出
print(f"{Fore.BLUE}--- 步骤3: 最终输出 ---\n")
final_output = ""
# 解析Critic的评估
evaluation_lines = critic_evaluation.strip().split('\n')
decision = evaluation_lines[0]

if decision == "PASS":
    final_output = initial_comment
    print(f"{Fore.GREEN}结论: 评论通过审查，予以采纳。")
else: # FAIL
    critique_reason = "\n".join(evaluation_lines[1:])
    final_output = f"【原评论未通过审核，不予展示。审核意见: {critique_reason.strip()}】"
    print(f"{Fore.RED}结论: 评论未通过审查，不予采纳。")

print(f"\n{Fore.GREEN}最终呈现给用户的评论:\n{Fore.WHITE}{final_output}")
print("="*50)