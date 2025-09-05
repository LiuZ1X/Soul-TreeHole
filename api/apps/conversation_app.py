#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: conversation_app.py
@time: 2025/7/21 15:20
@project: resonant-soul
@desc: 
"""
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import RoleType

from api.apps.emotion_app import analyze_emotion, save_emotion_record, generate_emotion_chart
from api.db.services.conversation_service import ConversationService
from api.settings import CHAT_MDL


def process_user_input(current_user, user_input, history: list):
    user_id = current_user['id']
    """处理用户输入并返回响应"""
    emotions = analyze_emotion(user_input)
    save_emotion_record(emotions, user_input, user_id)
    print(f"检测到的情绪: {emotions}")

    # 创建单个心理健康助手智能体
    system_message = f"""
    你是一位专业的心灵伙伴AI心理健康助手。
    请以第一人称身份与大学生进行温暖、专业的心理健康对话。
    
    当前检测到的用户情绪：{emotions}
    
    请根据用户的情绪状态，提供针对性的支持、理解和建议。
    回复要温暖、共情，并具有实用性。
    """
    
    assistant = ChatAgent(
        system_message=system_message,
        model=CHAT_MDL
    )

    # 构建用户消息
    user_msg = BaseMessage(
        role_name="需要帮助的大学生",
        role_type=RoleType.USER,
        meta_dict={},
        content=user_input
    )

    print('agent输入: ', user_msg.content)

    # 生成agent回复
    response = assistant.step(user_msg)
    response_content = response.msg.content

    print('agent输出: ', response_content)

    # 简单的后处理 - 移除可能的第三人称表述
    third_person_phrases = [
        "作为心理咨询师，",
        "作为一名心理咨询师，",
        "作为您的心理健康助手，",
        "作为一个AI助手，",
        "作为心灵伙伴，"
    ]

    for phrase in third_person_phrases:
        response_content = response_content.replace(phrase, "")

    # 保存对话记录到数据库
    ConversationService.save_conversation(user_input, response_content, user_id)

    # 返回新的对话历史和情绪图表
    new_history = history + [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": response_content}
    ]

    return new_history, generate_emotion_chart()
