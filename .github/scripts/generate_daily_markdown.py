import datetime
import requests
from bs4 import BeautifulSoup

def fetch_trending(language=None, count=10):
    url = "https://github.com/trending"
    if language:
        url += f"?since=daily&spoken_language_code=&l={language}"
    else:
        url += "?since=daily"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(resp.text, "html.parser")
    repo_elements = soup.find_all("article", class_="Box-row")
    repos = []
    for r in repo_elements[:count]:
        repo_name = r.h2.a["href"].strip("/")
        repo_url = f"https://github.com/{repo_name}"
        desc = r.p.text.strip() if r.p else ""
        repos.append((repo_name, repo_url, desc))
    return repos

def fetch_trending_multi_langs(langs, total):
    repos = []
    for lang in langs:
        needed = total - len(repos)
        if needed <= 0:
            break
        lang_repos = fetch_trending(lang, count=needed)
        for repo in lang_repos:
            if repo not in repos:
                repos.append(repo)
    return repos[:total]

def fetch_trending_all(count=50):
    return fetch_trending(None, count=count)

def markdown_section(title, repos):
    md = f"## {title}\n\n"
    for idx, (name, url, desc) in enumerate(repos, 1):
        line = f"{idx}. [{name}]({url})"
        if desc:
            line += f" — {desc}"
        md += line + "\n"
    return md

if __name__ == "__main__":
    today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    filename = f"{today}-github-recommendations.md"

    # 选择前端相关语言
    frontend_langs = ["JavaScript", "TypeScript", "HTML", "CSS", "Vue", "React", "Angular"]
    frontend_repos = fetch_trending_multi_langs(frontend_langs, 10)
    all_repos = fetch_trending_all(50)

    content = f"# {today} GitHub 推荐仓库\n\n"
    content += markdown_section("前端相关仓库（10 个）", frontend_repos)
    content += "\n"
    content += markdown_section("全站热门仓库（50 个）", all_repos)
    content += "\n---\n\n> 本文档由 Copilot Space 自动生成，用于每日 GitHub 优质项目推荐。\n"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)