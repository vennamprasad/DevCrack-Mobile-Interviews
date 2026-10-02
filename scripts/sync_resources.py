#!/usr/bin/env python3
"""
Dynamic Resource Manager & GitHub Sync Tool for Awesome Mobile Interviews.

Usage:
  # 1. Add a new repository dynamically:
  python3 scripts/sync_resources.py add "raamcosta/compose-destinations" --category android --section ui_toolkits

  # 2. Validate all repositories (check for 404s and live stars):
  python3 scripts/sync_resources.py validate

  # 3. Rebuild all markdown resource files from JSON catalog:
  python3 scripts/sync_resources.py build
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(REPO_ROOT, "resources", "data", "curated_repos.json")
RESOURCES_DIR = os.path.join(REPO_ROOT, "resources")

CATEGORY_FILE_MAP = {
    "android": "01-awesome-android-repos.md",
    "ios": "02-awesome-ios-repos.md",
    "cross_platform": "03-awesome-cross-platform-repos.md",
    "tooling_and_security": "04-mobile-system-design-and-tooling-repos.md"
}

CATEGORY_EMOJI_MAP = {
    "android": "📱",
    "ios": "🍎",
    "cross_platform": "🌉",
    "tooling_and_security": "📐"
}

def fetch_github_repo_info(repo_full_name: str) -> dict:
    url = f"https://api.github.com/repos/{repo_full_name}"
    headers = {"User-Agent": "Awesome-Mobile-Interviews-Sync/1.0"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
        
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "name": data.get("full_name", repo_full_name),
                "stars": data.get("stargazers_count", 0),
                "description": data.get("description", ""),
                "language": data.get("language", ""),
                "archived": data.get("archived", False),
                "pushed_at": data.get("pushed_at", "")
            }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ValueError(f"Repository '{repo_full_name}' was not found on GitHub (HTTP 404).")
        raise RuntimeError(f"GitHub API error for '{repo_full_name}': {e}")
    except Exception as e:
        raise RuntimeError(f"Network error querying '{repo_full_name}': {e}")

def load_catalog() -> dict:
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_catalog(catalog: dict):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

def generate_markdown_for_category(category_key: str, category_data: dict) -> str:
    emoji = CATEGORY_EMOJI_MAP.get(category_key, "📱")
    title = category_data.get("title", f"{category_key.title()} Repositories")
    desc = category_data.get("description", "")
    
    lines = [
        f"# {emoji} {title}",
        "",
        f"> **{desc}**",
        "",
        "---",
        ""
    ]
    
    for i, section in enumerate(category_data.get("sections", []), start=1):
        sec_title = section.get("title", f"Section {i}")
        lines.append(f"## 🏛️ {i}. {sec_title}" if i == 1 else f"## 🛠️ {i}. {sec_title}" if i == 2 else f"## 🎨 {i}. {sec_title}")
        lines.append("")
        
        # Determine column headers based on category/section
        is_blueprints = "blueprint" in section.get("id", "").lower() or "app" in section.get("title", "").lower()
        
        if is_blueprints:
            lines.append("| Repository | Stars | Tech Stack | Why You Should Study It |")
            lines.append("|:---|:---:|:---|:---|")
            for repo in section.get("repos", []):
                name = repo["name"]
                stack = repo.get("tech_stack", "")
                r_desc = repo.get("description", "")
                badge = f"[![Stars](https://img.shields.io/github/stars/{name}?style=social)](https://github.com/{name})"
                lines.append(f"| [**{name}**](https://github.com/{name}) | {badge} | {stack} | {r_desc} |")
        else:
            lines.append("| Library | Stars | Author / Tech | Purpose / Description |")
            lines.append("|:---|:---:|:---|:---|")
            for repo in section.get("repos", []):
                name = repo["name"]
                stack = repo.get("tech_stack", "")
                r_desc = repo.get("description", "")
                badge = f"[![Stars](https://img.shields.io/github/stars/{name}?style=social)](https://github.com/{name})"
                lines.append(f"| [**{name}**](https://github.com/{name}) | {badge} | {stack} | {r_desc} |")
        
        lines.append("")
        lines.append("---")
        lines.append("")
        
    # Remove trailing separator
    if lines[-2] == "---":
        lines.pop()
        lines.pop()
        
    return "\n".join(lines).strip() + "\n"

def build_all_markdowns():
    catalog = load_catalog()
    for cat_key, cat_data in catalog.items():
        if cat_key not in CATEGORY_FILE_MAP:
            continue
        filename = CATEGORY_FILE_MAP[cat_key]
        filepath = os.path.join(RESOURCES_DIR, filename)
        content = generate_markdown_for_category(cat_key, cat_data)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Generated: resources/{filename}")

def add_repo(repo_name: str, category: str, section_id: str, tech_stack: str = None, description: str = None):
    catalog = load_catalog()
    if category not in catalog:
        raise ValueError(f"Invalid category '{category}'. Choices: {list(catalog.keys())}")
    
    print(f"🔍 Fetching live details for '{repo_name}' from GitHub API...")
    info = fetch_github_repo_info(repo_name)
    actual_name = info["name"]
    
    cat_data = catalog[category]
    target_section = None
    for sec in cat_data.get("sections", []):
        if sec.get("id") == section_id:
            target_section = sec
            break
            
    if not target_section:
        sec_ids = [s.get("id") for s in cat_data.get("sections", [])]
        raise ValueError(f"Section '{section_id}' not found in category '{category}'. Available sections: {sec_ids}")
        
    final_tech = tech_stack or info.get("language") or "Mobile / Kotlin / Swift"
    final_desc = description or info.get("description") or "Open source production resource."
    
    # Check if already exists
    existing_idx = -1
    for i, r in enumerate(target_section.get("repos", [])):
        if r["name"].lower() == actual_name.lower():
            existing_idx = i
            break
            
    repo_entry = {
        "name": actual_name,
        "tech_stack": final_tech,
        "description": final_desc
    }
    
    if existing_idx >= 0:
        target_section["repos"][existing_idx] = repo_entry
        print(f"🔄 Updated existing repository: {actual_name} ({info['stars']:,} ⭐)")
    else:
        target_section["repos"].append(repo_entry)
        print(f"✨ Added new repository: {actual_name} ({info['stars']:,} ⭐)")
        
    save_catalog(catalog)
    build_all_markdowns()
    print("🎉 All markdown resource tables successfully updated!")

def validate_all():
    catalog = load_catalog()
    total_repos = 0
    errors = 0
    print("🚀 Validating all repositories against GitHub REST API...\n")
    
    for cat_key, cat_data in catalog.items():
        print(f"📂 Category: {cat_key}")
        for sec in cat_data.get("sections", []):
            print(f"  └─ Section: {sec.get('id')}")
            for r in sec.get("repos", []):
                total_repos += 1
                name = r["name"]
                try:
                    info = fetch_github_repo_info(name)
                    status = "⚠️ Archived" if info["archived"] else "✅ Active"
                    print(f"     • {name:<45} {info['stars']:>7,} ⭐  [{status}]")
                except Exception as e:
                    print(f"     ❌ {name:<45} ERROR: {e}")
                    errors += 1
                    
    print(f"\n==========================================")
    print(f"Total Scanned: {total_repos} repositories")
    print(f"Errors Found:  {errors}")
    print(f"==========================================")
    if errors > 0:
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Awesome Mobile Interviews Dynamic Resource Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # add command
    add_parser = subparsers.add_parser("add", help="Add or update a repository dynamically")
    add_parser.add_argument("repo", help="Repository in 'owner/repo' format (e.g. android/nowinandroid)")
    add_parser.add_argument("--category", required=True, choices=["android", "ios", "cross_platform", "tooling_and_security"])
    add_parser.add_argument("--section", required=True, help="Section ID (e.g. blueprints, libraries, ui_toolkits, flutter, react_native, kmp, security, telemetry)")
    add_parser.add_argument("--tech", help="Custom tech stack / author label")
    add_parser.add_argument("--desc", help="Custom description / highlight reason")
    
    # validate command
    subparsers.add_parser("validate", help="Validate all repositories against GitHub API")
    
    # build command
    subparsers.add_parser("build", help="Regenerate all markdown tables from JSON catalog")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_repo(args.repo, args.category, args.section, args.tech, args.desc)
    elif args.command == "validate":
        validate_all()
    elif args.command == "build":
        build_all_markdowns()

if __name__ == "__main__":
    main()
