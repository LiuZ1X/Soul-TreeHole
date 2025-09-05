#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: emotion_app.py
@time: 2025/7/21 14:56
@project: resonant-soul
@desc: 
"""
import json
from datetime import datetime
import torch
import matplotlib.pyplot as plt

try:
    from api.db.services.emotion_service import EmotionService
    from api.settings import EMOTION_RECORDS
except ImportError:
    print("ImportError in api/apps/emotion_app.py")

import os
# 模型缓存路径
# current_dir = os.path.dirname(os.path.abspath(__file__))
# new_cache_dir = os.path.join(current_dir, "hf_model")
# new_cache_dir = "hf_model"
current_file_path = os.path.abspath(__file__)

# 从当前文件路径向上回溯三次，找到项目根目录
# .../api/apps/emotion_app.py -> .../api/apps/ -> .../api/ -> .../
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))

# 将项目根目录与模型文件夹名拼接成一个绝对路径
new_cache_dir = os.path.join(project_root, "hf_model")
print(f"--- DEBUG: emotion_app.py calculated model cache path: {new_cache_dir} ---")
os.environ['HF_HOME'] = new_cache_dir
os.environ['HUGGINGFACE_HUB_CACHE'] = os.path.join(new_cache_dir, 'hub')

from transformers import pipeline
from transformers import BertForSequenceClassification
from transformers import BertTokenizer

class EmotionAnalyzer:
    def __init__(self, using_pipeline=True):
        self.classifier = None
        self.using_pipeline = using_pipeline
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        if using_pipeline:
            self._init_pipeline()
        else:
            self._init_naive()
    
    def _init_pipeline(self):
        """初始化 pipeline"""
        try:
            self.classifier = pipeline(
                "text-classification",
                model="IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment",
                tokenizer="IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment",
                device=self.device
            )
        except Exception as e:
            print(f"Pipeline 初始化失败: {e}")

    def _init_naive(self):
        # 检查GPU可用性
        print(f"Using device: {self.device}")

        self.tokenizer=BertTokenizer.from_pretrained('IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment')
        self.model=BertForSequenceClassification.from_pretrained('IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment')
        self.model = self.model.to(self.device)

    def analyze(self, text)-> dict[str, float] | None:
        if self.using_pipeline:
            return self.analyze_pipline(text)
        else:
            return self.analyze_torch(text)

    def analyze_pipline(self, text: str) -> dict[str, float] | None:
        """分析情绪  pipline方式"""
        if self.classifier is None:
            return None
        
        try:
            results = self.classifier(text)
            return results[0] if results else None
        except Exception as e:
            print(f"情绪分析失败: {e}")
            return None
        
    def analyze_torch(self, text: str) -> dict[str, float] | None:
        """使用 Torch 方式分析情绪"""
        input_tensor = torch.tensor([self.tokenizer.encode(text)]).to(self.device)
        
        with torch.no_grad():  # 推理时不需要梯度，节省内存
            output = self.model(input_tensor)
            scores = torch.nn.functional.softmax(output.logits, dim=-1)
        
        labels = ["Negative", "Positive"]
        return {"label": labels[scores.argmax()], "score": scores.max().item()}
        
        
# 全局实例化
emotion_analyzer = EmotionAnalyzer(using_pipeline = False)

def analyze_emotion(text):
    """用户情感分析：

    两种预训练模/简单规则的方式：
    1. tabularisai/multilingual-sentiment-analysis
    2. IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment
    """



    # """
    # # 使用tabularisai/multilingual-sentiment-analysi
    # """
    
    # classifier = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis", device=0)
    
    # result = classifier(text)[0]
    # label = result['label']
    # score = result['score']
    # print(result)

    # labels_en_2_zn = {"Very Negative":"超坏心情",  "Negative":"坏心情", "Neutral":"平静", "Positive":"好心情", "Very Positive:":"超好心情"}
    # zn_emo_label = labels_en_2_zn.get(label)

    # return [zn_emo_label] if zn_emo_label else ['平静']

    """
    # 使用IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment
    """
    result = emotion_analyzer.analyze(text)
    print(f"情绪分析结果: {result}")
    if result is None:
        return '平静'
    label = result['label']
    score = result['score']
    labels_en_2_zn = {"Negative":"坏心情", "Positive":"好心情"}
    zn_emo_label = labels_en_2_zn.get(label)
    # return [zn_emo_label] if score > 0.8 else ['平静']

    detected_emotions = []
    if score > 0.75:
        detected_emotions.append(zn_emo_label)
    else:
        detected_emotions.append('平静')

    """
    # 规则方式补充
    """
    emotions = {
        '焦虑': ['焦虑', '紧张', '不安', '担心', '压力', '烦恼', '心慌', '恐慌', '心悸', '坐立不安', '忧心忡忡', '忐忑', '烦躁', '神经质'],
        '抑郁': ['抑郁', '难过', '消沉', '伤心', '悲伤', '失落', '沮丧', '绝望', '郁闷', '颓废', '无助', '萎靡', '悲观', '情绪低落'],
        '愤怒': ['生气', '愤怒', '烦躁', '恼火', '不满', '讨厌', '怒火', '愤慨', '气愤', '暴躁', '怨恨', '敌意', '不耐烦', '暴怒'],
        '恐惧': ['害怕', '恐惧', '惊恐', '恐慌', '畏惧', '胆怯', '不安', '心惊', '毛骨悚然', '惶恐', '惊慌', '恐怖', '吓坏'],
        '厌恶': ['厌恶', '恶心', '反感', '讨厌', '嫌弃', '憎恶', '鄙视', '轻蔑', '不屑', '厌烦', '痛恨'],
        '惊讶': ['惊讶', '吃惊', '震惊', '意外', '诧异', '惊奇', '目瞪口呆', '震撼', '意想不到', '骇人听闻'],
        '积极': ['开心', '快乐', '高兴', '兴奋', '满足', '幸福', '愉悦', '欣喜', '乐观', '积极', '充满希望', '欣慰', '得意', '自豪'],
        '悲伤': ['悲伤', '伤心', '难过', '悲痛', '哀伤', '悲哀', '凄惨', '心碎', '泪丧', '郁郁寡欢', '苦闷', '忧愁'],
        '期待': ['期待', '盼望', '期望', '渴望', '憧憬', '向往', '希望', '热切', '焦急等待', '望眼欲穿'],
        '爱': ['爱', '喜欢', '疼爱', '宠爱', '钟爱', '热爱', '倾心', '迷恋', '爱慕', '深情', '温柔', '体贴'],
        '羞愧': ['羞愧', '惭愧', '尴尬', '难为情', '不好意思', '内疚', '自责', '懊悔', '耻辱', '丢脸', '自责'],
        '孤独': ['孤独', '孤单', '寂寞', '孤立', '冷清', '无人问津', '形单影只', '与世隔绝'],
        '平静': ['平静', '安宁', '宁静', '祥和', '安心', '放松', '镇定', '从容', '心如止水', '恬淡']
    }

    for emotion, keywords in emotions.items():
        if any(keyword in text for keyword in keywords):
            detected_emotions.append(emotion)

    return detected_emotions if detected_emotions else ['平静']


def save_emotion_record(emotion, user_input, user_id):
    """保存情绪记录"""
    record = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'emotion': emotion,
    }
    EMOTION_RECORDS.append(record)
    record['user_input'] = user_input
    # 添加数据库存储
    EmotionService.save_emotion(emotion, user_input, user_id)


def generate_emotion_chart():
    """生成情绪趋势图表"""
    if not EMOTION_RECORDS:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, 'No Emotion Data', ha='center', va='center')
        ax.set_axis_off()
        return fig

    # emotion_en_map = {
    #     '焦虑': 'Anxiety',
    #     '抑郁': 'Depression',
    #     '愤怒': 'Anger',
    #     '积极': 'Positive',
    #     '平静': 'Calm'
    # }
    emotion_en_map = {
        '好心情': 'Nice Mood',
        '坏心情': 'Bad Mood',
        '平静': 'Calm'
    }


    emotion_counts = {}
    for record in EMOTION_RECORDS:
        for emotion in record['emotion']:
            if emotion in emotion_counts:
                emotion_counts[emotion] += 1
            else:
                emotion_counts[emotion] = 1

    fig, ax = plt.subplots()
    labels = list(emotion_counts.keys())
    sizes = list(emotion_counts.values())
    labels_en = [emotion_en_map.get(label, label) for label in labels]

    # colors = {
    #     '焦虑': 'orange',
    #     '抑郁': 'blue',
    #     '愤怒': 'red',
    #     '积极': 'green',
    #     '平静': 'gray'
    # }
    colors = {
        '好心情': 'blue',
        '坏心情': 'orange',
        '平静': 'gray'
    }

    color_list = [colors.get(label, 'gray') for label in labels]
    ax.pie(sizes, labels=labels_en, autopct='%1.1f%%', colors=color_list)
    ax.set_title('Emotion Distribution')

    return fig


def get_all_emotion_records(user_id):
    """
    获取所有的情绪记录，并按照 date, content, emotions 的数组返回，数组里存放着每一个字典。
    """
    records = []
    # 获取所有情绪记录
    emotions = EmotionService.get_recent_all_emotions(user_id)
    for timestamp, emotion_json, user_input in emotions:
        emotions_list = json.loads(emotion_json)
        record = {
            "date": timestamp,
            "content": user_input,
            "emotions": emotions_list
        }
        records.append(record)
    return records



if __name__ == "__main__":
    test_text = "今天在食堂刷卡时余额不足，后面排队的男生直接帮我付了钱。我慌张道谢，他说‘上次我饭卡没钱你也帮过我呀’...完全想不起他是谁。原来陌生人之间也会像洋葱一样，剥开冷淡的外皮藏着暖意。"

    print(f"score: {emotion_analyzer.analyze(test_text)}")
    print(f"score: {emotion_analyzer.analyze('下雨了。出门正好又没有带伞无语了')}")