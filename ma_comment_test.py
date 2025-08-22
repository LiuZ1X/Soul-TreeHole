from pyfiglet import Figlet

# # 使用不同字体风格
# f = Figlet()
# print(f.renderText('Soul Tree Hole'))

# # 区块风格
# f = Figlet(font='block')
# print(f.renderText('TreeHole'))


from colorama import Fore
from camel.societies import RolePlaying
from camel.utils import print_text_animated
from camel.models import ModelFactory
from camel.types import ModelPlatformType
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
user_input = text_list[1]
# user_input = text_list[random.randint(0,9)]

# emotions = ["快乐", "悲伤", "愤怒", "惊讶", "恐惧"][1]
# user_input = "59分比0分更扎心！期末考翻车了查分那刻我人没了...微积分59！离及格就差1分啊啊啊！教授你是懂精准打击的！！翻车现场还原,考前一晚：自信满满刷某音“3小时速成微积分”.考试当天：看到卷子瞬间瞳孔地震。交卷时：把选择题填串行直接送走10分..."

def main(model=CHAT_MDL, chat_turn_limit=3) -> None:
    # Initialize a session for developing a trading bot
    """
    RolePlaying:回合制、提示引擎驱动、零角色翻转
        TASK:一个目标或想法，以简单的提示形式给出。
        AI USER:负责提供指令或挑战的角色。
        AI ASSISTANT:负责生成解决方案、计划或逐步响应的角色。
        CRITIC(可选)：一个负责审查或评价助手响应质量的角色。
    """

    # task_prompt = "用口语化、网络化、积极向上的语言治愈他人，友善地对他人进行评论和心理上的鼓励"
    task_prompt = f"请以一位善于用语言治愈他人的陌生网友的身份。根据检测到的情绪{emotions}，请对学生的帖子进行回复，要求回答口语化、接地气、语气积极。帖子: {user_input}"
    role_play_session = RolePlaying(
        assistant_role_name="一位善良的陌生网友",
        assistant_agent_kwargs=dict(model=model),
        user_role_name="需要帮助的大学生",
        user_agent_kwargs=dict(model=model),
        task_prompt=task_prompt,
        with_task_specify=False,
        task_specify_agent_kwargs=dict(model=model),
        output_language='中文'
  )

    # Print initial system messages
    print(
        Fore.GREEN
        + f"AI Assistant sys message:\n{role_play_session.assistant_sys_msg}"
    )
    print(
        Fore.BLUE + f"AI User sys message:\n{role_play_session.user_sys_msg}"
    )

    print(Fore.YELLOW + f"Original task prompt:\n{task_prompt}")
    print(
        Fore.CYAN
        + "Specified task prompt:"
        + f"\n{role_play_session.specified_task_prompt}"
    )
    print(Fore.RED + f"Final task prompt:\n{role_play_session.task_prompt}")

    n = 0
    input_msg = role_play_session.init_chat()


    # input_msg = role_play_session.init_chat()
    # # input_msg.content = f"""
    # # Instruction: 请以一位善于用语言治愈他人的AI助手的身份回应。根据检测到的情绪 {emotions}，对学生的帖子进行回复，要求回答口语化和网络化，语气活泼。
    # # Input: {user_input}
    # # """

    # print(Fore.WHITE+ f"input_msg:\n{input_msg}")
    # # print(input_msg.content)

    # assistant_response, user_response = role_play_session.step(input_msg)
    # input_msg = assistant_response.msg
    # print(user_response.msg.content)
    # print('------------------------------------------')
    # print(assistant_response.msg.content)

    # Turn-based simulation
    while n < chat_turn_limit:
        n += 1
        assistant_response, user_response = role_play_session.step(input_msg)

        if assistant_response.terminated:
            print(
                Fore.GREEN
                + (
                    "AI Assistant terminated. Reason: "
                    f"{assistant_response.info['termination_reasons']}."
                )
            )
            break
        if user_response.terminated:
            print(
                Fore.GREEN
                + (
                    "AI User terminated. "
                    f"Reason: {user_response.info['termination_reasons']}."
                )
            )
            break

        print(
            Fore.BLUE + f"AI User:\n\n{user_response.msg.content}\n"
        )
        print(
            Fore.GREEN + "AI Assistant:\n\n"
            f"{assistant_response.msg.content}\n"
        )

        if "CAMEL_TASK_DONE" in user_response.msg.content:
            break

        input_msg = assistant_response.msg

if __name__ == "__main__":
  main()