from app.questgen.topic import Topic
from typing import List
import random

class Subject:

    def __init__(self, name, topics: List, description):
        self.name = name
        self.desc = description
        self._load_topics(topics)

    def _load_topics(self, topic_list):
        topics = []
        for i in topic_list:
            topics.append(Topic(desc=i["content"]))
        self.topics = topics
    
    def get_topic(self):
        return random.choice(self.topics)



    
