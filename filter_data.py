import json
import re

def filter_data(lines):
    filtered = []

    keywords = [
        r'harina',
        r'garbanzo',
        r'sal',
        r'agua'
    ]

    exclusions = []

    for entry in lines:
        text_lower = entry['text'].lower()
        page = entry['page']

        if any(re.search(exc, text_lower) for exc in exclusions):
            continue

        for kw in keywords:
            if re.search(kw, text_lower):
                filtered.append({
                    'page': page,
                    'text': entry['text']
                })
                break
    return filtered

def main():
    with open('extracted_data.json', 'r') as f:
        lines = json.load(f)

    result = filter_data(lines)

    with open('filtered_data.json', 'w') as f2:
        json.dump(result, f2, indent=4)

    print(f'Se han encontrado {len(result)} líneas relevantes. Guardadas en filtered_data.json')

if __name__ == '__main__':
    main()

