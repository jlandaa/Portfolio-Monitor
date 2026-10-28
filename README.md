# ⚙️ Portfolio Monitor: DataOps & CI/CD Automation

![Uptime](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/jlandaa/portfolio-monitor/main/uptime.json)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)](https://www.selenium.dev/)

## 📝 Descripción General

Este repositorio funciona como el "cuarto de máquinas" (*engine room*) de mi ecosistema de proyectos de datos. Es un microservicio **serverless** diseñado para garantizar la alta disponibilidad (HA) de todas las aplicaciones interactivas e interfaces de Machine Learning alojadas en mi portafolio.

Debido a que las plataformas de *hosting* gratuitas (como Streamlit Community Cloud) suspenden los contenedores tras períodos de inactividad, desarrollé esta infraestructura de monitoreo automatizado para prevenir el *Sleep Mode* y asegurar que los reclutadores y usuarios siempre experimenten tiempos de carga instantáneos (Cold Start = 0).

## 🚀 Arquitectura y Flujo de Trabajo

El sistema opera de forma 100% autónoma utilizando **GitHub Actions** como orquestador principal:

1. **Cron Job Programado:** Un flujo de trabajo CI/CD (`keep_awake.yml`) se dispara automáticamente cada 4 horas.
2. **Health Check Automatizado:** Levanta un entorno Ubuntu virtual, instala dependencias e inicializa un navegador Chrome en modo *Headless*.
3. **Simulación de Tráfico (Selenium):** El script `keep_awake.py` navega iterativamente por las URLs de producción del ecosistema (Sales AI Chatbot, ADR Dashboard, SmartCredit-ML). Evalúa el DOM de la página y, si detecta la pantalla de hibernación de Streamlit, interactúa con los elementos web para reiniciar el contenedor.
4. **Reporte de Estado (SLA):** Tras validar la disponibilidad, el script compila el estado de salud de la infraestructura en un archivo `uptime.json`.
5. **Git Push Automatizado:** El bot de GitHub Actions realiza un *commit* silencioso con el nuevo JSON, actualizando en tiempo real el *badge* dinámico visible en la [página principal de mi perfil](https://github.com/jlandaa).

## 📂 Estructura del Repositorio

La arquitectura se mantiene minimalista y orientada a un único propósito (*Single Responsibility Principle*):

```text
📦 Portfolio-Monitor
 ┣ 📂 .github/workflows
 ┃ ┗ 📜 keep_awake.yml    # Orquestador CI/CD (Cron jobs y ejecución de scripts)
 ┣ 📜 keep_awake.py       # Script principal de Web Automation (Selenium WebDriver)
 ┣ 📜 requirements.txt    # Dependencias del entorno virtual (selenium)
 ┣ 📜 uptime.json         # Archivo de estado dinámico consumido por Shields.io
 ┗ 📜 README.md           # Documentación técnica
