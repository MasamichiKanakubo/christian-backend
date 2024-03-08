import json

with open("app/use_cases/scrapbox/faqs.json", "r", encoding="utf-8") as file:
    data = json.load(file)

def find_value_for_question(question, data):
    for item in data:
        if question in item:
            return item[question]

print(find_value_for_question("男女比はどの程度ですか？", data))
