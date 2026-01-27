import requests
import os

# 環境変数から情報を取得（GitHubのSecretsに設定します）
USER_ID = os.environ['ZOTERO_USER_ID']
API_KEY = os.environ['ZOTERO_API_KEY']
VERSION_FILE = 'last_version.txt' # 前回読み込んだ時のバージョンを記録するファイル
# 特定のコレクションのみ対象にする場合はそのID、ライブラリ全体なら 'items'
URL = f'https://api.zotero.org/users/{USER_ID}/items?format=json&limit=100'

def fetch_zotero():
    headers = {'Zotero-API-Key': API_KEY}
    response = requests.get(URL, headers=headers)
    current_version = response.headers.get('Last-Modified-Version')
    
    # 2. 前回のバージョンを確認
    last_version = ""
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'r') as f:
            last_version = f.read().strip()

    # 3. バージョンが変わっていなければ終了
    if current_version == last_version:
        print("Not changed")
        return False

    # 4. 変更があった場合のみMarkdownを生成
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

    # 5. 新しいバージョン番号を保存
    with open(VERSION_FILE, 'w') as f:
        f.write(current_version)
    
    return True

if __name__ == "__main__":
    if fetch_zotero():
        print("更新が完了しました。")
    else:
        exit(0) # 変更がない場合は正常終了（GitHub ActionsでCommitさせないため）
