import requests
import os

# 環境変数から情報を取得（GitHubのSecretsに設定します）
USER_ID = os.environ['ZOTERO_USER_ID']
API_KEY = os.environ['ZOTERO_API_KEY']
# 特定のコレクションのみ対象にする場合はそのID、ライブラリ全体なら 'items'
URL = f'https://api.zotero.org/users/{USER_ID}/items?format=json&limit=100'

def fetch_zotero():
    headers = {'Zotero-API-Key': API_KEY}
    response = requests.get(URL, headers=headers)
    items = response.json()
    
    with open('literature_list.md', 'w', encoding='utf-8') as f:
        f.write("# Zotero My Library\n\n")
        for item in items:
            data = item.get('data', {})
            # 親アイテム（論文等）のみを抽出
            if 'title' in data:
                title = data.get('title').replace('{', '').replace('}', '')
                author_list = [a.get('lastName', '') for a in data.get('creators', [])]
                authors = ", ".join(author_list)
                year = data.get('date', 'N/A')
                abstract = data.get('abstractNote', 'なし')
                
                f.write(f"## {title}\n")
                f.write(f"- **Auther**: {authors}\n")
                f.write(f"- **Publication**: {year}\n")
                f.write(f"- **Abstract**: {abstract}\n\n")

if __name__ == "__main__":
    fetch_zotero()
