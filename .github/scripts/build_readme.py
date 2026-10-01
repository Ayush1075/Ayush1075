"""
Builds README.md from README.template.md using live data from the GitHub API.

Tokens you can use in README.template.md:
  {{USERNAME}}                 -> your GitHub username
  {{REPO:kw1|kw2}}             -> link to your repo whose name contains any keyword
  {{DEMO_LINK:kw1|kw2}}        -> " · [Live Demo](url)" from the repo's Website field, or nothing
  {{STARS:kw1|kw2}}            -> star count of that repo
  {{LINKEDIN_BADGE}}           -> LinkedIn badge (from repo variable or your GitHub social links)
  {{LATEST_REPOS}}             -> table of your most recently updated repos (excluding featured ones)
  {{UPDATED}}                  -> date of last refresh
"""
import json, os, re, sys, urllib.request, datetime

USER = os.environ.get("GH_USER", "").strip()
TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
LINKEDIN_OVERRIDE = os.environ.get("LINKEDIN_URL", "").strip()
TEMPLATE = os.environ.get("TEMPLATE_PATH", "README.template.md")
OUTPUT = os.environ.get("OUTPUT_PATH", "README.md")
LATEST_COUNT = 6

if not USER:
    sys.exit("GH_USER is not set")


def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "profile-readme-builder")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def fetch_repos():
    repos, page = [], 1
    while True:
        batch = api(f"/users/{USER}/repos?per_page=100&page={page}&type=owner&sort=pushed")
        if not batch:
            break
        repos.extend(batch)
        page += 1
    return [r for r in repos if not r.get("private")]


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


repos = fetch_repos()
used = set()


def find_repo(keywords):
    keys = [norm(k) for k in keywords.split("|") if k.strip()]
    candidates = []
    for r in repos:
        if r.get("fork"):
            continue
        name = norm(r["name"])
        for k in keys:
            if k and k in name:
                exact = 1 if name == k else 0
                candidates.append((exact, r.get("stargazers_count", 0), r.get("pushed_at", ""), r))
                break
    if not candidates:
        return None
    candidates.sort(key=lambda c: (c[0], c[1], c[2]), reverse=True)
    repo = candidates[0][3]
    used.add(repo["name"])
    return repo


def repo_link(m):
    r = find_repo(m.group(1))
    return r["html_url"] if r else f"https://github.com/{USER}?tab=repositories"


def demo_link(m):
    r = find_repo(m.group(1))
    home = (r or {}).get("homepage") or ""
    return f" · [Live Demo]({home})" if home.strip() else ""


def stars(m):
    r = find_repo(m.group(1))
    return str(r.get("stargazers_count", 0)) if r else "0"


def linkedin_badge():
    url = LINKEDIN_OVERRIDE
    if not url:
        try:
            for acc in api(f"/users/{USER}/social_accounts"):
                if acc.get("provider") == "linkedin" or "linkedin.com" in acc.get("url", ""):
                    url = acc["url"]
                    break
        except Exception as e:
            print("Could not read social accounts:", e)
    if not url:
        return ""
    return (f'<a href="{url}"><img src="https://img.shields.io/badge/LinkedIn-0A66C2'
            f'?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>')


def latest_table():
    rows = []
    for r in repos:
        if r.get("fork") or r.get("archived") or r["name"] in used:
            continue
        if r["name"].lower() == USER.lower():
            continue
        desc = (r.get("description") or "No description yet").replace("|", "/").strip()
        lang = r.get("language") or "-"
        pushed = (r.get("pushed_at") or "")[:10]
        demo = f" · [Live]({r['homepage']})" if (r.get("homepage") or "").strip() else ""
        rows.append(f"| [**{r['name']}**]({r['html_url']}){demo} | {desc} | `{lang}` | ⭐ {r.get('stargazers_count', 0)} | {pushed} |")
        if len(rows) >= LATEST_COUNT:
            break
    if not rows:
        return "_More projects coming soon._"
    head = "| Repository | What it does | Language | Stars | Last updated |\n|---|---|---|---|---|"
    return head + "\n" + "\n".join(rows)


with open(TEMPLATE, encoding="utf-8") as f:
    text = f.read()

# Drop the editing note at the top of the template from the published README
text = re.sub(r"\A\s*<!--.*?-->\s*", "", text, count=1, flags=re.S)
text = text.replace("{{USERNAME}}", USER)
# Featured tokens first, so LATEST_REPOS can skip repos already shown
text = re.sub(r"\{\{REPO:([^}]+)\}\}", repo_link, text)
text = re.sub(r"\{\{DEMO_LINK:([^}]+)\}\}", demo_link, text)
text = re.sub(r"\{\{STARS:([^}]+)\}\}", stars, text)
text = text.replace("{{LINKEDIN_BADGE}}", linkedin_badge())
text = text.replace("{{LATEST_REPOS}}", latest_table())
text = text.replace("{{UPDATED}}", datetime.date.today().strftime("%d %b %Y"))

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(text)

print(f"README built for {USER}: {len(repos)} public repos, featured matched: {sorted(used)}")
