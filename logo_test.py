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
    model_config_dict={"temperature": 0.7},
)
emotions = ["快乐", "悲伤", "愤怒", "惊讶", "恐惧"][1]
user_input = "59分比0分更扎心！期末考翻车了查分那刻我人没了...微积分59！离及格就差1分啊啊啊！教授你是懂精准打击的！！翻车现场还原,考前一晚：自信满满刷某音“3小时速成微积分”.考试当天：看到卷子瞬间瞳孔地震。交卷时：把选择题填串行直接送走10分..."

def main(model=CHAT_MDL, chat_turn_limit=3) -> None:
    # Initialize a session for developing a trading bot
    task_prompt = "用口语化、网络化、积极向上的语言治愈他人，友善地对他人进行评论和心理上的鼓励"
    role_play_session = RolePlaying(
        assistant_role_name="一位善于用语言治愈他人的AI助手",
        assistant_agent_kwargs=dict(model=model),
        user_role_name="在校大学生",
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
    input_msg = role_play_session.init_chat(
    f"""Instruction: 请以一位善于用语言治愈他人的AI助手的身份回应。根据检测到的情绪 {emotions}，对学生的帖子进行回复，要求回答口语化和网络化，语气活泼。
    Input: {user_input}
    """)

    # assistant_response, user_response = role_play_session.step(input_msg)
    # input_msg = assistant_response.msg

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