from camel.societies import RolePlaying

from api.apps.emotion_app import analyze_emotion, save_emotion_record, generate_emotion_chart
from api.db.services.conversation_service import ConversationService
from api.db.services.tree_hole_services import TreeHoleService
from api.settings import CHAT_MDL


#这里使用的Camel-AI进行单/多agent的智能回复行为




def auto_comment_treehole(treehole_id, comment_text, user_id=None, anonymous_id=None):
    """自动评论树洞内容"""
    # 这里可以调用Camel-AI的预设角色进行评论生成、自动点赞等功能
    
    # 创建角色会话 TODO

    # 初始化提示词 TODO

    # 调用大模型进行对话 TODO

    # 保存树洞内容到树洞数据库
    

class CounselorAgent:
    def respond(self, user_input):
        # 调用Camel-AI的预设心理咨询师角色
        return ai_engine.generate_response("counselor", user_input)

class ListenerAgent:
    def respond(self, user_input):
        # 简单的倾听者角色
        return f"我能感受到你的{emotion_analysis(user_input)}，请继续说。"