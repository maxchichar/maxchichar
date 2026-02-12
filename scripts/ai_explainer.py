import os
import requests

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

GITHUB_REPOS = [
    "sudoku",
    "networth-dashboard"
]

USERNAME = "maxchichar"


def get_readme(repo):
    url = f"https://raw.githubusercontent.com/{USERNAME}/{repo}/main/README.md"
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    return "No README found"


def generate_summary(text):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4.1-mini",
        "messages": [
            {"role": "system", "content": "Summarize this GitHub project professionally."},
            {"role": "user", "content": text[:3000]}
        ]
    }

    res = requests.post(url, headers=headers, json=data)
    return res.json()["choices"][0]["message"]["content"]


def build_output():
    output = "# 🤖 AI Project Summaries\n\n"

    for repo in GITHUB_REPOS:
        readme = get_readme(repo)
        summary = generate_summary(readme)

        output += f"## {repo}\n"
        output += summary + "\n\n"

    with open("AI_PROJECT_SUMMARIES.md", "w") as f:
        f.write(output)


if __name__ == "__main__":
    build_output()
