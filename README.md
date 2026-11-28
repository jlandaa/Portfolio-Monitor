# ⚙️ Portfolio Monitor: DataOps & CI/CD Observability

<p align="left">
  <a href="[https://github.com/jlandaa/Portfolio-Monitor/actions/workflows/keep_awake.yml](https://github.com/jlandaa/Portfolio-Monitor/actions/workflows/keep_awake.yml)"><img src="[https://raw.githubusercontent.com/jlandaa/Portfolio-Monitor/main/uptime.svg](https://raw.githubusercontent.com/jlandaa/Portfolio-Monitor/main/uptime.svg)" alt="Streamlit Apps Status" /></a>
  <a href="[https://github.com/jlandaa/Retail-Price-Scraper/actions/workflows/etl_fravega.yml](https://github.com/jlandaa/Retail-Price-Scraper/actions/workflows/etl_fravega.yml)"><img src="[https://raw.githubusercontent.com/jlandaa/Portfolio-Monitor/main/etl_status.svg](https://raw.githubusercontent.com/jlandaa/Portfolio-Monitor/main/etl_status.svg)" alt="ETL Frávega Status" /></a>
  <a href="[https://github.com/jlandaa/Portfolio-Monitor](https://github.com/jlandaa/Portfolio-Monitor)"><img src="[https://raw.githubusercontent.com/jlandaa/Portfolio-Monitor/main/ci_status.svg](https://raw.githubusercontent.com/jlandaa/Portfolio-Monitor/main/ci_status.svg)" alt="CI Quality Status" /></a>
</p>

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)](https://www.selenium.dev/)

## 📝 Descripción General

Este repositorio centraliza el monitoreo y la observabilidad **serverless** de mi portafolio de proyectos de datos. Opera de forma autónoma sobre **GitHub Actions** para cumplir dos funciones operativas:

1. **Alta Disponibilidad (HA) en Streamlit Cloud:** Evita que las aplicaciones interactivas entren en modo de hibernación (*Sleep Mode*) por inactividad, reduciendo tiempos de espera por *cold start* para quienes visitan el portafolio.
2. **Observabilidad de CI/CD & ETL + Badges SVG Propios:** Audita periódicamente el estado de los pipelines de calidad (`Ruff` + `Pytest`) y del ETL productivo de Frávega mediante la API REST de GitHub, generando archivos `.svg` estáticos servidos directamente desde GitHub para eliminar timeouts y dependencias externas de Shields.io.

## 🚀 Arquitectura y Flujo de Trabajo

El workflow `keep_awake.yml` orquesta el ciclo completo cada 4 horas (`0 */4 * * *`) y admite ejecución manual (`workflow_dispatch`):

1. **Health Check con Selenium (`keep_awake.py`):** Levanta Chrome en modo *Headless* sobre Ubuntu, recorre las aplicaciones productivas de Streamlit y, si detecta la pantalla de suspensión, interactúa con el DOM para reactivar el contenedor. Al finalizar escribe el estado en `uptime.json`.
2. **Auditoría de Pipelines (`check_ci_status.py`):** Utiliza únicamente la librería estándar de Python (`urllib`, `json`, `xml.sax.saxutils`) y `GITHUB_TOKEN` para consultar la última ejecución completada en `main` de los 4 workflows de CI y del ETL programado.
3. **Generación Autónoma de Badges SVG:** Renderiza `uptime.svg`, `ci_status.svg` y `etl_status.svg` en estilo `flat-square` (`#1E293B`), junto a sus respectivos `.json`, logrando carga instantánea en el [perfil principal](https://github.com/jlandaa) sin pasar por proxies de terceros.
4. **Commit Condicional (`github-actions[bot]`):** Compara cambios con `git diff --cached --quiet` y realiza `commit` + `push` únicamente si algún estado cambió realmente, manteniendo limpio el historial del repositorio.

## 📡 Ecosistema Monitoreado

| Componente | Alcance Monitoreado | Artefacto Generado |
| :--- | :--- | :--- |
| **Streamlit Apps** | Sales AI Chatbot, ADR Dashboard, Smart Credit ML | `uptime.json` / `uptime.svg` |
| **CI Quality (4/4)** | `ci.yml` en `Retail-Price-Scraper`, `ETL-ADR-Argentina`, `Sales-AI-Chatbot`, `Smart-Credit-ML` | `ci_status.json` / `ci_status.svg` |
| **ETL Productivo** | `etl_fravega.yml` en `Retail-Price-Scraper` | `etl_status.json` / `etl_status.svg` |

## 📂 Estructura del Repositorio

```text
📦 Portfolio-Monitor
 ┣ 📂 .github/workflows
 ┃ ┗ 📜 keep_awake.yml     # Orquestador programado cada 4h y commit condicional
 ┣ 📜 keep_awake.py        # Automatización Headless con Selenium para Streamlit Cloud
 ┣ 📜 check_ci_status.py   # Auditoría vía GitHub REST API y generador autónomo de SVG
 ┣ 📜 requirements.txt     # Dependencias del entorno (selenium)
 ┣ 📜 uptime.json / .svg   # Estado de disponibilidad de las apps de Streamlit
 ┣ 📜 ci_status.json / .svg # Estado consolidado de los 4 workflows de CI (Ruff & Pytest)
 ┣ 📜 etl_status.json / .svg # Estado independiente del pipeline ETL de Frávega
 ┗ 📜 README.md            # Documentación técnica
