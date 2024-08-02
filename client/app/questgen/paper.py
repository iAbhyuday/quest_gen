import json
import random
import pkg_resources
from typing import List
from app.questgen.subject import Subject

class Paper:
    def __init__(self, name:str):
        self.name = name
        self.subjects = []
        self._load_subjects("syllabus.json")

    def _load_subjects(self, filename):
        syllabus = {}
        syllabus_path = pkg_resources.resource_filename('app', f'config/{filename}')
        with open(syllabus_path, 'r') as syl:
            syllabus = json.load(syl)[self.name]
        
        for k, v in syllabus.items():
            self.subjects.append(Subject(name=k, topics=v["topics"], description=v["Description"]))
    
    def get_subject(self, subject=None):
        if subject is not None:
            return subject
        return random.choice(self.subjects)
        
            


    
