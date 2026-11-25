import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DESCRIPTION_LIMIT = 400
errors = []


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        errors.append(f"{path}: sem frontmatter")
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(": ")
        value = value.strip()
        if value.startswith("'") and value.endswith("'"):
            value = value[1:-1].replace("''", "'")
        elif ": " in value:
            errors.append(f"{path}: '{key}' tem ': ' sem aspas, o YAML quebra")
        fields[key] = value
    return fields


def check_versions():
    claude = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
    codex = json.loads((ROOT / "plugin.json").read_text())
    json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
    if claude["version"] != codex["version"]:
        errors.append(f"versão diferente: .claude-plugin/plugin.json {claude['version']} x plugin.json {codex['version']}")


def check_skills():
    agents_text = "".join(p.read_text(encoding="utf-8") for p in (ROOT / "agents").glob("zero-to-sys-*.md"))
    skills = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
    for skill_file in (ROOT / "skills").glob("*/SKILL.md"):
        fields = frontmatter(skill_file)
        name = skill_file.parent.name
        if fields.get("name") != name:
            errors.append(f"{skill_file}: name '{fields.get('name')}' diferente da pasta")
        if len(fields.get("description", "")) > DESCRIPTION_LIMIT:
            errors.append(f"{skill_file}: descrição com {len(fields['description'])} caracteres (limite {DESCRIPTION_LIMIT})")
        if name != "zero-to-sys" and f"| `{name}` |" not in agents_text:
            errors.append(f"skill '{name}' não está na tabela de nenhum agente especialista")
    for cited in set(re.findall(r"^\| `([a-z-]+)` \|", agents_text, re.M)):
        if cited not in skills:
            errors.append(f"agente cita a skill '{cited}', que não existe")
    for agent_file in (ROOT / "agents").glob("*.md"):
        frontmatter(agent_file)


def check_links():
    for md in ROOT.rglob("*.md"):
        if ".git" in md.parts or "specs" in md.parts:
            continue
        text = re.sub(r"```.*?```", "", md.read_text(encoding="utf-8"), flags=re.S)
        for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (md.parent / target).exists():
                errors.append(f"{md.relative_to(ROOT)}: link quebrado para {target}")


check_versions()
check_skills()
check_links()
for error in errors:
    print(error)
print(f"{len(errors)} problema(s)")
sys.exit(1 if errors else 0)
