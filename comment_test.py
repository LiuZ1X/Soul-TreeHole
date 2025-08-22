from pyfiglet import Figlet
from colorama import Fore

from camel.utils import print_text_animated
from camel.models import ModelFactory
from camel.types import ModelPlatformType
from camel.agents import ChatAgent
from camel.messages import BaseMessage
# from api.settings import CHAT_MDL

CHAT_MDL = ModelFactory.create(
    model_platform=ModelPlatformType.OLLAMA,
    model_type="qwen2.5:7b",
    model_config_dict={"temperature": 0.7, 'max_tokens':4096},
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
emo_of_textlist = ['疲惫+愤怒',"委屈+孤独", "温暖+触动", "悸动+甜蜜", "绝望+自我怀疑", "尴尬+孤立感", "惊喜+雀跃", "感动+释然", "心酸+无奈", "清醒+坚定"]
import random

emotions = emo_of_textlist[1]
user_input = text_list[7]

from camel.types import RoleType

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
- 熟练运用网络热梗和缩写
- 评论常常以意想不到的结论结尾。
# 格式与约束
- 可以只玩梗，不直接评价帖子内容。
"""
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


cot_prompt = """
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
4.  **最终评论是**: ...
<SOLUTION>

**开始任务**
"""


assistants = []
for sys_msg in sys_msgs:
    assistants.append(ChatAgent(
        system_message=sys_msg,
        model=CHAT_MDL,
        output_language='中文'
    ))

# for assistant in assistants:
#     print(assistant.system_message.content)

# rand_assistant = random.choice(assistants)
rand_assistant = assistants[1]
print(rand_assistant.system_message.content)

user_msg  = BaseMessage(
    role_name = "需要帮助的大学生",
    role_type= RoleType.USER,
    meta_dict={},
    content= f"""{cot_prompt} 请结合你的身份，评论以下这篇的帖子：{user_input}"""
)

response = rand_assistant.step(user_msg)

print(response.msg.content)