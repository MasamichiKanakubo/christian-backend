import os
import re
import requests
import json
from itertools import product
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


# class ScrapboxRepository:
#     def __init__(self, scrapbox_project_name: str):
#         self.scrapbox_project_name = scrapbox_project_name
#         self.question_re_pattarn = re.compile(r"\?")

#     def fetch_page_data(self, title: str):
#         response = requests.get(
#             f"https://scrapbox.io/api/pages/{self.scrapbox_project_name}/{title}"
#         ).json()
#         return response

#     def get_faqs(self) -> List[dict]:
#         url = f"https://scrapbox.io/api/pages/{self.scrapbox_project_name}"
#         response = requests.get(url).json()
#         titles = [page["title"] for page in response["pages"]]
#         response_list: list = []
#         with ThreadPoolExecutor(max_workers=10) as executor:
#             future_to_title = {
#                 executor.submit(self.fetch_page_data, title): title for title in titles
#             }
#             for future in as_completed(future_to_title):
#                 res = future.result()
#                 page_title = res["title"]
#                 lines = res.get("lines", [])

#                 questions: list = []
#                 for line in lines:
#                     text = line.get("text", "")
#                     if self.question_re_pattarn.search(text):
#                         cleaned_text = re.sub(r"\? ", "", text).strip("`")
#                         questions.extend(self.convert_text_to_questions(cleaned_text))

#                 if questions:
#                     response_list.append(
#                         {"page_title": page_title, "questions": questions}
#                     )

#         return response_list

#     def generate_combinations(self, options_list: List[str]) -> List[tuple]:
#         return list(product(*options_list))

#     def apply_combination(self, text: str, combination):
#         for option in combination:
#             match = re.search(r"\((.+?)\)", text)
#             if match:
#                 text = text.replace(match.group(0), option, 1)
#         return text
    
#     def convert_text_to_questions(self, text: str):
#         matches = re.finditer(r"\((.+?)\)", text)
#         options_list = [match.group(1).split("|") for match in matches]

#         combinations = self.generate_combinations(options_list)

#         return [
#             self.apply_combination(text, combination) for combination in combinations
#         ]


# scrapbox_repository = ScrapboxRepository(os.getenv("SCRAPBOX_PROJECT_NAME"))
# faqs = scrapbox_repository.get_faqs()
# for faq in faqs:
#     print(faq)