"""
Builds README.md + animated SVGs in assets/ from README.template.md and live GitHub data.

Template tokens:
  {{USERNAME}}  {{REPO:kw1|kw2}}  {{DEMO_LINK:kw1|kw2}}  {{STARS:kw1|kw2}}
  {{LINKEDIN_BADGE}}  {{LATEST_REPOS}}  {{UPDATED}}
Generated assets (dark + light):
  hero, terminal, stats, languages, footer
"""
import json, os, re, sys, urllib.request, datetime, html

USER = os.environ.get("GH_USER", "").strip()
TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
LINKEDIN_OVERRIDE = os.environ.get("LINKEDIN_URL", "").strip()
TEMPLATE = os.environ.get("TEMPLATE_PATH", "README.template.md")
OUTPUT = os.environ.get("OUTPUT_PATH", "README.md")
ASSETS = os.environ.get("ASSETS_DIR", "assets")
LATEST_COUNT = 6

# ---------- Personal content (edit freely) ----------
NAME = "Ayush Gupta"
ROLE = "Full-Stack Engineer · AI Systems Builder"
SCHOOL = "B.Tech CSE @ BML Munjal University · Class of 2027"
STATUS = "Open to SDE / Full-Stack / AI Engineering roles"
TAGS = ["Graph RAG", "Computer Vision", "FastAPI", "MERN", "Docker"]
WHOAMI = "Ayush Gupta · Full-Stack & AI Engineer · BMU CSE '27"
NOW = [
    "Building CodeJanitor: an AI agent that patches vulnerabilities pre-merge",
    "Exploring agentic AI, retrieval systems & explainable ML",
    "Odoo Hackathon 2026 Finalist · Flipkart GRiD 8.0 Semi-Finalist",
]
# ----------------------------------------------------

if not USER:
    sys.exit("GH_USER is not set")

PALETTES = {
    "dark": dict(bg="#0d1117", panel="#161b22", border="#30363d", text="#e6edf3", muted="#8b949e",
                 accent="#2f81f7", accent2="#a371f7", green="#3fb950", orb=0.45, grid=0.06),
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de", text="#1f2328", muted="#656d76",
                  accent="#0969da", accent2="#8250df", green="#1a7f37", orb=0.22, grid=0.08),
}
SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
MONO = "'SF Mono', 'Cascadia Code', Consolas, 'Liberation Mono', Menlo, monospace"
LANG_COLORS = {"Python": "#3572A5", "JavaScript": "#f1e05a", "TypeScript": "#3178c6", "C++": "#f34b7d",
               "Java": "#b07219", "C#": "#178600", "HTML": "#e34c26", "CSS": "#563d7c",
               "Jupyter Notebook": "#DA5B0B", "Shell": "#89e051", "Go": "#00ADD8", "C": "#555555",
               "Dart": "#00B4AB", "Kotlin": "#A97BFF", "ShaderLab": "#222c37", "Dockerfile": "#384d54"}


def esc(s):
    return html.escape(str(s), quote=True)


def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "profile-readme-builder")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def safe(fn, default):
    try:
        return fn()
    except Exception as e:
        print("warning:", e)
        return default


def fetch_repos():
    repos, page = [], 1
    while True:
        batch = api(f"/users/{USER}/repos?per_page=100&page={page}&type=owner&sort=pushed")
        if not batch:
            break
        repos.extend(batch)
        page += 1
    return [r for r in repos if not r.get("private")]


repos = fetch_repos()
profile = safe(lambda: api(f"/users/{USER}"), {})
events = safe(lambda: api(f"/users/{USER}/events/public?per_page=100"), [])
own = [r for r in repos if not r.get("fork") and r["name"].lower() != USER.lower()]
used = set()


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def find_repo(keywords):
    keys = [norm(k) for k in keywords.split("|") if k.strip()]
    cands = []
    for r in own:
        name = norm(r["name"])
        for k in keys:
            if k and k in name:
                cands.append((name == k, r.get("stargazers_count", 0), r.get("pushed_at", ""), r))
                break
    if not cands:
        return None
    cands.sort(key=lambda c: c[:3], reverse=True)
    used.add(cands[0][3]["name"])
    return cands[0][3]


# ======================= SVG GENERATORS =======================

def svg_hero(p):
    W, H = 900, 270
    orbs = ""
    for i, (cx, cy, r, col, dx, dy, d) in enumerate([
        (120, 60, 130, p["accent"], 60, 30, 14), (780, 210, 150, p["accent2"], -70, -25, 17),
        (520, -20, 110, p["green"], -40, 40, 19)]):
        orbs += (f'<circle class="orb o{i}" cx="{cx}" cy="{cy}" r="{r}" fill="{col}" opacity="{p["orb"]}" filter="url(#blur)"/>'
                 f'<style>.o{i}{{animation:drift{i} {d}s ease-in-out infinite alternate}}'
                 f'@keyframes drift{i}{{to{{transform:translate({dx}px,{dy}px)}}}}</style>')
    tags, x = "", 0
    for t in TAGS:
        w = len(t) * 7.4 + 22
        tags += (f'<g transform="translate({x},0)"><rect width="{w:.0f}" height="24" rx="12" fill="{p["panel"]}" '
                 f'stroke="{p["border"]}"/><text x="{w/2:.0f}" y="16.5" text-anchor="middle" class="tag">{esc(t)}</text></g>')
        x += w + 8
    tag_x = (W - (x - 8)) / 2
    pill_w = len(STATUS) * 7.1 + 46
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(NAME)}: {esc(ROLE)}">
<defs>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="45"/></filter>
  <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="{p["text"]}" stroke-opacity="{p["grid"]}"/></pattern>
  <linearGradient id="g" x1="0" x2="1">
    <stop offset="0" stop-color="{p["accent"]}"/><stop offset=".5" stop-color="{p["accent2"]}"/><stop offset="1" stop-color="{p["accent"]}"/>
    <animate attributeName="x1" values="0;-1;0" dur="8s" repeatCount="indefinite"/>
    <animate attributeName="x2" values="1;2;1" dur="8s" repeatCount="indefinite"/>
  </linearGradient>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath>
</defs>
<style>
  .orb{{transform-box:fill-box;transform-origin:center}}
  .name{{font:700 48px {SANS};fill:{p["text"]};opacity:0;animation:up .9s ease-out .1s forwards}}
  .role{{font:600 21px {SANS};opacity:0;animation:up .9s ease-out .45s forwards}}
  .school{{font:400 15px {SANS};fill:{p["muted"]};opacity:0;animation:up .9s ease-out .75s forwards}}
  .tags{{opacity:0;animation:up .9s ease-out 1.05s forwards}}
  .tag{{font:500 12px {MONO};fill:{p["muted"]}}}
  .pill{{opacity:0;animation:up .9s ease-out 1.35s forwards}}
  .status{{font:600 12.5px {SANS};fill:{p["green"]}}}
  .pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2s ease-out infinite}}
  @keyframes up{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}
  @keyframes pulse{{0%{{transform:scale(1);opacity:.7}}100%{{transform:scale(2.8);opacity:0}}}}
</style>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="{p["bg"]}"/>
  {orbs}
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{p["border"]}"/>
<text x="{W/2}" y="92" text-anchor="middle" class="name">{esc(NAME)}</text>
<text x="{W/2}" y="128" text-anchor="middle" class="role" fill="url(#g)">{esc(ROLE)}</text>
<text x="{W/2}" y="156" text-anchor="middle" class="school">{esc(SCHOOL)}</text>
<g class="tags"><g transform="translate({tag_x:.0f},176)">{tags}</g></g>
<g transform="translate({(W-pill_w)/2:.0f},218)"><g class="pill">
  <rect width="{pill_w:.0f}" height="28" rx="14" fill="{p["green"]}" fill-opacity=".12" stroke="{p["green"]}" stroke-opacity=".5"/>
  <circle class="pulse" cx="18" cy="14" r="4" fill="{p["green"]}"/><circle cx="18" cy="14" r="4" fill="{p["green"]}"/>
  <text x="32" y="18.5" class="status">{esc(STATUS)}</text>
</g></g>
</svg>'''


def rel_time(iso):
    if not iso:
        return "recently"
    then = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    days = (datetime.datetime.now(datetime.timezone.utc) - then).days
    return "today" if days < 1 else "yesterday" if days == 1 else f"{days} days ago"


def terminal_lines():
    stars = sum(r.get("stargazers_count", 0) for r in own)
    langs = {}
    for r in own:
        if r.get("language"):
            langs[r["language"]] = langs.get(r["language"], 0) + 1
    top = max(langs, key=langs.get) if langs else "Python"
    last = own[0].get("pushed_at") if own else None
    lines = [("cmd", "whoami"), ("out", WHOAMI), ("cmd", "cat now.txt")]
    lines += [("out", "→ " + n) for n in NOW]
    lines += [("cmd", "gh stats --live"),
              ("hl", f"repos: {len(own)}  ·  stars: {stars}  ·  top language: {top}  ·  last push: {rel_time(last)}")]
    commits = []
    for e in events:
        if e.get("type") == "PushEvent":
            repo = e["repo"]["name"].split("/")[-1]
            if repo.lower() == USER.lower():
                continue
            for c in reversed(e.get("payload", {}).get("commits", [])):
                msg = c.get("message", "").splitlines()[0] if c.get("message") else ""
                if msg and not msg.lower().startswith("merge"):
                    commits.append((c.get("sha", "")[:7], repo, msg))
        if len(commits) >= 3:
            break
    if commits:
        lines.append(("cmd", "git log --all --oneline -3"))
        for sha, repo, msg in commits[:3]:
            lines.append(("log", (sha, f"{repo}: {msg}")))
    elif own:
        lines.append(("cmd", "ls -t ~/projects | head -3"))
        for r in own[:3]:
            lines.append(("out", f"{r['name']}   (updated {rel_time(r.get('pushed_at'))})"))
    return lines


def svg_terminal(p, lines):
    W, LH, TOP, FS, CW = 900, 24, 58, 14, 8.43
    MAXC = 96
    H = TOP + LH * (len(lines) + 1) + 16
    t = 0.6
    body = ""
    for i, (kind, val) in enumerate(lines):
        y = TOP + LH * i + 14
        if kind == "cmd":
            text = val[:MAXC]
            w = (len(text) + 2) * CW + 4
            steps = len(text)
            dur = max(0.35, steps * 0.045)
            vals = ";".join(f"{(2 + k) * CW + 2:.1f}" for k in range(steps + 1))
            body += (f'<clipPath id="c{i}"><rect x="20" y="{y-16}" height="22" width="{2*CW+2:.1f}">'
                     f'<animate attributeName="width" values="{vals}" calcMode="discrete" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>'
                     f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t-0.3:.2f}s" fill="freeze"/>'
                     f'<text x="24" y="{y}" clip-path="url(#c{i})"><tspan fill="{p["green"]}">$</tspan> <tspan fill="{p["text"]}">{esc(text)}</tspan></text></g>')
            t += dur + 0.35
        else:
            if kind == "log":
                sha, msg = val
                msg = msg if len(msg) <= MAXC - 10 else msg[:MAXC - 11] + "…"
                content = f'<tspan fill="{p["accent2"]}">{esc(sha)}</tspan>  <tspan fill="{p["text"]}">{esc(msg)}</tspan>'
            else:
                v = val if len(val) <= MAXC else val[:MAXC - 1] + "…"
                col = p["accent"] if kind == "hl" else p["muted"]
                content = f'<tspan fill="{col}">{esc(v)}</tspan>'
            body += (f'<text x="24" y="{y}" opacity="0">{content}'
                     f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur=".25s" fill="freeze"/></text>')
            t += 0.12
            nxt = lines[i + 1][0] if i + 1 < len(lines) else "end"
            if nxt == "cmd" or nxt == "end":
                t += 0.45
    y = TOP + LH * len(lines) + 14
    body += (f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'
             f'<text x="24" y="{y}" fill="{p["green"]}">$</text>'
             f'<rect x="{24 + 2*CW:.1f}" y="{y-13}" width="8" height="16" fill="{p["text"]}">'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect></g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal introduction">
<style>text{{font:400 {FS}px {MONO};white-space:pre}}</style>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{p["panel"]}" stroke="{p["border"]}"/>
<path d="M.5 12.5a12 12 0 0 1 12-12h{W-25}a12 12 0 0 1 12 12V36H.5z" fill="{p["bg"]}" stroke="{p["border"]}"/>
<circle cx="22" cy="18" r="6" fill="#ff5f57"/><circle cx="42" cy="18" r="6" fill="#febc2e"/><circle cx="62" cy="18" r="6" fill="#28c840"/>
<text x="{W/2}" y="22.5" text-anchor="middle" fill="{p["muted"]}" style="font-size:12.5px">{esc(USER)}@github: ~</text>
{body}
</svg>'''


def svg_stats(p):
    stars = sum(r.get("stargazers_count", 0) for r in own)
    forks = sum(r.get("forks_count", 0) for r in own)
    created = profile.get("created_at")
    since = created[:4] if created else "—"
    items = [("Public repos", len(own)), ("Stars earned", stars), ("Forks", forks),
             ("Followers", profile.get("followers", 0)), ("On GitHub since", since)]
    W, H = 440, 210
    rows = ""
    for i, (k, v) in enumerate(items):
        y = 72 + i * 27
        rows += (f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{0.3 + i*0.15:.2f}s" dur=".4s" fill="freeze"/>'
                 f'<circle cx="30" cy="{y-5}" r="4" fill="{p["accent"]}"/>'
                 f'<text x="44" y="{y}" class="k">{esc(k)}</text><text x="{W-28}" y="{y}" text-anchor="end" class="v">{esc(v)}</text></g>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="GitHub stats">
<style>.t{{font:600 17px {SANS};fill:{p["text"]}}}.k{{font:400 14px {SANS};fill:{p["muted"]}}}.v{{font:700 14px {SANS};fill:{p["text"]}}}</style>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{p["panel"]}" stroke="{p["border"]}"/>
<text x="24" y="38" class="t">GitHub at a glance</text>
{rows}
</svg>'''


def svg_langs(p):
    counts = {}
    for r in own:
        if r.get("language"):
            counts[r["language"]] = counts.get(r["language"], 0) + 1
    top = sorted(counts.items(), key=lambda kv: -kv[1])[:5] or [("Python", 1)]
    total = sum(counts.values()) or 1
    W, H, BW = 440, 210, 225
    rows = ""
    for i, (lang, n) in enumerate(top):
        y = 66 + i * 28
        pct = n / total
        col = LANG_COLORS.get(lang, p["accent"])
        rows += (f'<text x="24" y="{y+10}" class="k">{esc(lang)}</text>'
                 f'<rect x="138" y="{y}" width="{BW}" height="12" rx="6" fill="{p["border"]}" fill-opacity=".5"/>'
                 f'<rect x="138" y="{y}" width="0" height="12" rx="6" fill="{col}">'
                 f'<animate attributeName="width" from="0" to="{max(12, BW*pct):.0f}" begin="{0.3+i*0.15:.2f}s" dur="1s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/></rect>'
                 f'<text x="{W-24}" y="{y+10}" text-anchor="end" class="v">{pct*100:.0f}%</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Top languages">
<style>.t{{font:600 17px {SANS};fill:{p["text"]}}}.k{{font:400 13.5px {SANS};fill:{p["muted"]}}}.v{{font:600 12.5px {SANS};fill:{p["text"]}}}</style>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{p["panel"]}" stroke="{p["border"]}"/>
<text x="24" y="38" class="t">Languages across my repos</text>
{rows}
</svg>'''


def svg_footer(p):
    W, H = 900, 110
    a = "M0 60 C150 30 300 90 450 60 S750 30 900 60 V110 H0Z"
    b = "M0 60 C150 90 300 30 450 60 S750 90 900 60 V110 H0Z"
    c = "M0 75 C200 55 350 95 500 75 S800 55 900 75 V110 H0Z"
    d = "M0 75 C200 95 350 55 500 75 S800 95 900 75 V110 H0Z"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Footer">
<defs><linearGradient id="f" x1="0" x2="1"><stop offset="0" stop-color="{p["accent"]}"/><stop offset="1" stop-color="{p["accent2"]}"/></linearGradient></defs>
<path fill="url(#f)" opacity=".35" d="{a}"><animate attributeName="d" values="{a};{b};{a}" dur="9s" repeatCount="indefinite"/></path>
<path fill="url(#f)" opacity=".75" d="{c}"><animate attributeName="d" values="{c};{d};{c}" dur="7s" repeatCount="indefinite"/></path>
<text x="{W/2}" y="30" text-anchor="middle" style="font:500 14px {SANS};fill:{p["muted"]}">Build · Think · Adapt · Demo</text>
</svg>'''


def write_assets():
    os.makedirs(ASSETS, exist_ok=True)
    lines = terminal_lines()
    for mode, p in PALETTES.items():
        for name, svg in [("hero", svg_hero(p)), ("terminal", svg_terminal(p, lines)),
                          ("stats", svg_stats(p)), ("languages", svg_langs(p)), ("footer", svg_footer(p))]:
            with open(f"{ASSETS}/{name}-{mode}.svg", "w", encoding="utf-8") as f:
                f.write(svg)


# ======================= README TOKENS =======================

def repo_link(m):
    r = find_repo(m.group(1))
    return r["html_url"] if r else f"https://github.com/{USER}?tab=repositories"


def demo_link(m):
    home = ((find_repo(m.group(1)) or {}).get("homepage") or "").strip()
    return f" · [Live Demo]({home})" if home else ""


def stars(m):
    r = find_repo(m.group(1))
    return str(r.get("stargazers_count", 0)) if r else "0"


def linkedin_badge():
    url = LINKEDIN_OVERRIDE
    if not url:
        for acc in safe(lambda: api(f"/users/{USER}/social_accounts"), []):
            if acc.get("provider") == "linkedin" or "linkedin.com" in acc.get("url", ""):
                url = acc["url"]
                break
    if not url:
        return ""
    return (f'<a href="{url}"><img src="https://img.shields.io/badge/LinkedIn-0A66C2'
            f'?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>')


def latest_table():
    rows = []
    for r in own:
        if r.get("archived") or r["name"] in used:
            continue
        desc = (r.get("description") or "No description yet").replace("|", "/").strip()
        demo = f" · [Live]({r['homepage']})" if (r.get("homepage") or "").strip() else ""
        rows.append(f"| [**{r['name']}**]({r['html_url']}){demo} | {desc} | `{r.get('language') or '-'}` | ⭐ {r.get('stargazers_count', 0)} | {(r.get('pushed_at') or '')[:10]} |")
        if len(rows) >= LATEST_COUNT:
            break
    if not rows:
        return "_More projects coming soon._"
    return "| Repository | What it does | Language | Stars | Last updated |\n|---|---|---|---|---|\n" + "\n".join(rows)


with open(TEMPLATE, encoding="utf-8") as f:
    text = f.read()

text = re.sub(r"\A\s*<!--.*?-->\s*", "", text, count=1, flags=re.S)
text = text.replace("{{USERNAME}}", USER)
text = re.sub(r"\{\{REPO:([^}]+)\}\}", repo_link, text)
text = re.sub(r"\{\{DEMO_LINK:([^}]+)\}\}", demo_link, text)
text = re.sub(r"\{\{STARS:([^}]+)\}\}", stars, text)
text = text.replace("{{LINKEDIN_BADGE}}", linkedin_badge())
text = text.replace("{{LATEST_REPOS}}", latest_table())
text = text.replace("{{UPDATED}}", datetime.date.today().strftime("%d %b %Y"))

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(text)
write_assets()
print(f"Built README + assets for {USER}: {len(own)} repos, featured: {sorted(used)}")
