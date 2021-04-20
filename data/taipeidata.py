import json

with open ("taipei.json","r", encoding="utf-8") as f:
    data = json.load(f)
    data = data["result"]["results"]

print(len(data))
print(data)
