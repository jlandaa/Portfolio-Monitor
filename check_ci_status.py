import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

WORKFLOWS = [
    ("jlandaa", "Retail-Price-Scraper", "etl_fravega.yml"),
    ("jlandaa", "Retail-Price-Scraper", "ci.yml"),
    ("jlandaa", "ETL-ADR-Argentina", "ci.yml"),
    ("jlandaa", "Sales-AI-Chatbot", "ci.yml"),
    ("jlandaa", "Smart-Credit-ML", "ci.yml"),
]

OUTPUT_FILE = Path("ci_status.json")


def consultar_ultimo_estado(owner: str, repo: str, workflow: str, token: str | None) -> bool:
    """Consulta la última ejecución completada en main y devuelve True si cerró en success."""
    url = (
        f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/"
        f"{workflow}/runs?branch=main&status=completed&per_page=1"
    )
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "jlandaa-portfolio-monitor",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"[WARN] No se pudo consultar {repo}/{workflow}: {exc}")
        return False

    runs = data.get("workflow_runs", [])
    if not runs:
        print(f"[WARN] Sin ejecuciones completadas en {repo}/{workflow}")
        return False

    conclusion = runs[0].get("conclusion")
    print(f"[OK] {repo}/{workflow} -> {conclusion}")
    return conclusion == "success"


def construir_payload_badge(aprobados: int, total: int) -> dict[str, object]:
    """Construye el JSON compatible con Shields.io Endpoint Badge."""
    if aprobados == total:
        color = "brightgreen"
    elif aprobados > 0:
        color = "yellow"
    else:
        color = "red"

    return {
        "schemaVersion": 1,
        "label": "CI & ETL PIPELINES",
        "message": f"{aprobados}/{total} PASSING",
        "color": color,
    }


def main() -> None:
    token = os.getenv("GITHUB_TOKEN")
    aprobados = sum(
        consultar_ultimo_estado(owner, repo, workflow, token)
        for owner, repo, workflow in WORKFLOWS
    )
    payload = construir_payload_badge(aprobados, len(WORKFLOWS))
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Archivo generado: {OUTPUT_FILE} -> {payload['message']}")


if __name__ == "__main__":
    main()
