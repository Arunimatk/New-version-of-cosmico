import json

# Configuration
DATA_FILE = 'data.json'
PREFIX_TO_REMOVE = 'https://cosmico-backend-arun.onrender.com/media/'
PREFIX_TO_REMOVE_2 = 'http://127.0.0.1:8000/media/' # In case some are local

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

count = 0
for item in data:
    if item['model'] == 'api.product':
        image_path = item['fields'].get('image', '')
        if image_path:
            if image_path.startswith(PREFIX_TO_REMOVE):
                item['fields']['image'] = image_path.replace(PREFIX_TO_REMOVE, '')
                count += 1
            elif image_path.startswith(PREFIX_TO_REMOVE_2):
                item['fields']['image'] = image_path.replace(PREFIX_TO_REMOVE_2, '')
                count += 1
            # Also clean up any double slashes if present
            # item['fields']['image'] = item['fields']['image'].lstrip('/')

with open(DATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Fixed {count} image paths in {DATA_FILE}")
