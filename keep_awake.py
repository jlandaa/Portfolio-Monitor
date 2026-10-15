from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import json

# Lista de las aplicaciones del portfolio
URLS = [
    "https://jml-ventas-ai.streamlit.app/", # Chatbot de ventas híbrido
    "https://jml-dashboard-adr.streamlit.app/", # URL del dashboard de ADRs argentinos
    "https://jml-smartcredit-ml.streamlit.app/"  # URL de la app SmartCredit-ML
]

def ping_streamlit_apps():
    options = Options()
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # 1 VITAL INICIALIZA LA VARIABLE
    todas_las_apps_ok = True 

    try:
        driver = webdriver.Chrome(options=options)
        
        for url in URLS:
            print(f"Iniciando visita a: {url}")
            try:
                driver.get(url)
                
                print("Buscando el botón para despertar la app...")
                boton_despertar = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Yes, get this app back up!')]"))
                )
                boton_despertar.click()
                print("¡Botón presionado! Esperando 30 segundos para que la app arranque...")
                time.sleep(30)
                
            except TimeoutException:
                # El botón no está -> La app está perfecta. NO cambiamos la variable a False.
                print("El botón no apareció. La app ya estaba activa.")
                time.sleep(5)
            except Exception as e_inner:
                # Un error real (ej. la página no carga)
                print(f"Ocurrió un error real cargando {url}: {e_inner}")
                todas_las_apps_ok = False 
            
            print(f"Visita completada para: {url}\n")
            
        print("Todas las aplicaciones del portfolio fueron visitadas. Cerrando navegador.")
        driver.quit()
        
    except Exception as e:
        print(f"Ocurrió un error crítico con el navegador: {e}")
        todas_las_apps_ok = False 

    # Armamos y guardamos el JSON
    badge_data = {
        "schemaVersion": 1,
        "label": "STREAMLIT APPS",
        "message": "ONLINE" if todas_las_apps_ok else "OFFLINE",
        "color": "success" if todas_las_apps_ok else "critical",
        "style": "for-the-badge"
    }

    try:
        with open("uptime.json", "w") as f:
            json.dump(badge_data, f)
        print("Archivo uptime.json generado correctamente.")
        
    except Exception as e:
        print(f"Error al guardar el archivo JSON: {e}")

if __name__ == "__main__":
    ping_streamlit_apps()
