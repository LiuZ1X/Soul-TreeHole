#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: settings.py
@time: 2025/7/21 14:58
@project: resonant-soul
@desc: 
"""

from camel.models import ModelFactory
from camel.types import ModelPlatformType
from dotenv import load_dotenv

from api.db.db_models import DBManager
from api.utils import get_base_config
from api.utils.t_crypt import decrypt_api_key, generate_key

EMOTION_RECORDS = []
databaseConn = None
CHAT_MDL = None
ADMIN_USER = None


def init_settings():
    global EMOTION_RECORDS, databaseConn, CHAT_MDL, ADMIN_USER
    # 存储情绪记录和日记
    databaseConn = DBManager()

    # 加载环境变量
    load_dotenv(dotenv_path='.env')

    LLM = get_base_config("llm")
    api_key = LLM['api_key']
    api_key = decrypt_api_key(api_key, generate_key())

    # 初始化模型， 联网API方式调用
    # CHAT_MDL = ModelFactory.create(
    #     model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
    #     model_type=LLM['model_type'],
    #     url=LLM['model_url'],
    #     api_key=api_key
    # )

    #初始化本地ollama 的qwen2.5:7B模型
    CHAT_MDL = ModelFactory.create(
        model_platform=ModelPlatformType.OLLAMA,
        model_type="qwen2.5:7b",
        model_config_dict={"temperature": 0.7},
    )

    ADMIN_USER = get_base_config("admin")
