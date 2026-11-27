import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape

WORKFLOWS = [
    ("jlandaa", "Retail-Price-Scraper", "etl_fravega.yml"),
    ("jlandaa", "Retail-Price-Scraper", "ci.yml"),
    ("jlandaa", "ETL-ADR-Argentina", "ci.yml"),
    ("jlandaa", "Sales-AI-Chatbot", "ci.yml"),
    ("jlandaa", "Smart-Credit-ML", "ci.yml"),
]

UPTIME_JSON = Path("uptime.json")
UPTIME_SVG = Path("uptime.svg")
CI_JSON = Path("ci_status.json")
CI_SVG = Path("ci_status.svg")

COLOR_MAP = {
    "brightgreen": "#4c1",
    "green": "#97ca00",
    "yellowgreen": "#a4a61d",
    "yellow": "#dfb317",
    "orange": "#fe7d37",
    "red": "#e05d44",
    "blue": "#007ec6",
    "lightgrey": "#9f9f9f",
}


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
    """Construye el diccionario de estado para los workflows de CI y ETL."""
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


def _normalizar_color(color: str) -> str:
    limpio = color.strip().lower()
    if limpio in COLOR_MAP:
        return COLOR_MAP[limpio]
    if limpio.startswith("#"):
        return limpio
    return f"#{limpio}" if len(limpio) in (3, 6) else "#4c1"


def _estimar_ancho_texto(texto: str) -> int:
    ancho = 0.0
    for ch in texto:
        if ch in " ilI1.,:;|!":
            ancho += 4.2
        elif ch in "MW@#%&":
            ancho += 9.5
        elif ch.isupper():
            ancho += 7.6
        else:
            ancho += 6.6
    return int(round(ancho)) + 16


def renderizar_badge_svg(
    label: str,
    message: str,
    color: str,
    label_color: str = "#1E293B",
) -> str:
    """Genera un SVG flat-square autónomo (sin dependencias de Shields.io)."""
    left_w = _estimar_ancho_texto(label)
    right_w = _estimar_ancho_texto(message)
    total_w = left_w + right_w

    left_x = left_w * 5
    right_x = left_w * 10 + right_w * 5

    label_esc = escape(label)
    msg_esc = escape(message)
    aria = escape(f"{label}: {message}")
    right_fill = _normalizar_color(color)

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="20" '
        f'role="img" aria-label="{aria}">'
        f"<title>{aria}</title>"
        '<g shape-rendering="crispEdges">'
        f'<rect width="{left_w}" height="20" fill="{label_color}"/>'
        f'<rect x="{left_w}" width="{right_w}" height="20" fill="{right_fill}"/>'
        "</g>"
        '<g fill="#fff" text-anchor="middle" '
        'font-family="Verdana,Geneva,DejaVu Sans,sans-serif" '
        'text-rendering="geometricPrecision" font-size="110">'
        f'<text x="{left_x}" y="140" transform="scale(.1)" fill="#fff">{label_esc}</text>'
        f'<text x="{right_x}" y="140" transform="scale(.1)" fill="#fff" '
        f'font-weight="bold">{msg_esc}</text>'
        "</g>"
        "</svg>\n"
    )


def main() -> None:
    token = os.getenv("GITHUB_TOKEN")
    aprobados = sum(
        consultar_ultimo_estado(owner, repo, workflow, token)
        for owner, repo, workflow in WORKFLOWS
    )
    ci_payload = construir_payload_badge(aprobados, len(WORKFLOWS))
    CI_JSON.write_text(json.dumps(ci_payload, indent=2) + "\n", encoding="utf-8")
    CI_SVG.write_text(
        renderizar_badge_svg(
            str(ci_payload["label"]),
            str(ci_payload["message"]),
            str(ci_payload["color"]),
        ),
        encoding="utf-8",
    )
    print(f"Generados {CI_JSON} y {CI_SVG} -> {ci_payload['message']}")

    if UPTIME_JSON.exists():
        uptime_data = json.loads(UPTIME_JSON.read_text(encoding="utf-8"))
        UPTIME_SVG.write_text(
            renderizar_badge_svg(
                str(uptime_data.get("label", "STREAMLIT APPS")),
                str(uptime_data.get("message", "ONLINE")),
                str(uptime_data.get("color", "brightgreen")),
            ),
            encoding="utf-8",
        )
        print(f"Generado {UPTIME_SVG} -> {uptime_data.get('message')}")


if __name__ == "__main__":
    main()
