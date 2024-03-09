import os
import re
import requests
import json
from itertools import product
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


class ScrapboxRepository:
    def __init__(self, scrapbox_project_name: str):
        self.scrapbox_project_name = scrapbox_project_name
        self.question_re_pattern = re.compile(r"\?")

    def get_scrapbox_answer(self, title: str):
        url = f"https://scrapbox.io/api/pages/{self.scrapbox_project_name}/{title}"
        response = requests.get(url).json()
        descriptions = response.get("descriptions", [])
        
        # 正規表現に一致しない説明のみをリストに含める
        descriptions_list = [
            description for description in descriptions
            if not self.question_re_pattern.search(description)
        ]
        return descriptions_list

