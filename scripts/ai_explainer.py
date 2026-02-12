import os
import requests

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
USERNAME = "maxchichar"

HEADERS = {
    "Authorization": f"Bearer {OPENAI_KEY}",
    "Content-Type": "application/json"
}


# 🔹 Fetch all public repos automatically
def get_repositories():
    url = f"https://api.github.com/users/{USERNAME}/repos"
    response = requests.get(url)
    repos = response.json()

    valid_repos = []

    for repo in repos:
        if not repo["fork"]:
            valid_repos.append(repo["name"])

    return valid_repos


# 🔹 Get README from repo
def get_readme(repo):
    url = f"https://raw.githubusercontent.com/{USERNAME}/{repo}/main/README.md"
    r = requests.get(url)

    if r.status_code == 200:
        return r.text

    return None


# 🔹 Generate AI summary
def generate_summary(text):

    url = "https://api.openai.com/v1/chat/completions"

    data = {
        "model": "gpt-4.1-mini",
        "messages": [
            {
                "role": "system",
                "content": "Explain this GitHub project in 3 concise professional sentences."
            },
            {
                "role": "user",
                "content": text[:2500]
            }
        ]
    }

    res = requests.post(url, headers=HEADERS, json=data)

    return res.json()["choices"][0]["message"]["content"]


# 🔹 Build output file automatically
def build_output():

    repos = get_repositories()

    output = "# 🤖 AI Generated Project Summaries\n\n"

    for repo in repos:

        readme = get_readme(repo)

        if readme:
            summary = generate_summary(readme)

            output += f"## {repo}\n"
            output += summary + "\n\n"

    with open("AI_PROJECT_SUMMARIES.md", "w") as f:
        f.write(output)


if __name__ == "__main__":
    build_output()
