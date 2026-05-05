import json

with open('ml/dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

data['intents'] = [i for i in data['intents'] if i['tag'] != 'general_search']

with open('ml/dataset.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Done! Intents left:', len(data['intents']))
print([i['tag'] for i in data['intents']])