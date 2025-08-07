from colorama import Fore
from camel.societies import RolePlaying
from camel.utils import print_text_animated
from camel.models import ModelFactory
from camel.types import ModelPlatformType

CHAT_MDL = ModelFactory.create(
    model_platform=ModelPlatformType.OLLAMA,
    model_type="qwen2.5:7b",
    model_config_dict={"temperature": 0.7},
)

def main(model=CHAT_MDL, chat_turn_limit=50) -> None:
  # Initialize a session for developing a trading bot
  task_prompt = "Develop a trading bot for the stock market"
  role_play_session = RolePlaying(
      assistant_role_name="Python Programmer",
      assistant_agent_kwargs=dict(model=model),
      user_role_name="Stock Trader",
      user_agent_kwargs=dict(model=model),
      task_prompt=task_prompt,
      with_task_specify=True,
      task_specify_agent_kwargs=dict(model=model),
      output_language='中文'
  )

  # Print initial system messages
  print(
      Fore.GREEN
      + f"AI Assistant sys message:\\n{role_play_session.assistant_sys_msg}\\n"
  )
  print(
      Fore.BLUE + f"AI User sys message:\\n{role_play_session.user_sys_msg}\\n"
  )

  print(Fore.YELLOW + f"Original task prompt:\\n{task_prompt}\\n")
  print(
      Fore.CYAN
      + "Specified task prompt:"
      + f"\\n{role_play_session.specified_task_prompt}\\n"
  )
  print(Fore.RED + f"Final task prompt:\\n{role_play_session.task_prompt}\\n")

  n = 0
  input_msg = role_play_session.init_chat()

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

      print_text_animated(
          Fore.BLUE + f"AI User:\\n\\n{user_response.msg.content}\\n"
      )
      print_text_animated(
          Fore.GREEN + "AI Assistant:\\n\\n"
          f"{assistant_response.msg.content}\\n"
      )

      if "CAMEL_TASK_DONE" in user_response.msg.content:
          break

      input_msg = assistant_response.msg

if __name__ == "__main__":
  main()