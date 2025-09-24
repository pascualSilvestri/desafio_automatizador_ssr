import sys
import os
import fnmatch

# Agregar el directorio padre al path para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import URL_PAGE, URL_USERNAME, URL_PASSWORD
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import glob
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class DownloadConfig:
    """Configuración para cada tipo de descarga"""
    button_id: str
    name: str
    requires_login: bool = False
    requires_checkboxes: bool = False
    download_patterns: List[str] = None
    file_name: str = "downloaded_file"


# Configuraciones para cada servicio
DOWNLOAD_CONFIGS = {
    "auto_express": DownloadConfig(
        button_id="download-button-autorepuestos-express",
        name="Autorepuestos Express",
        download_patterns=["AutoRepuestos Express*.csv", "AutoRepuestos Express*.xlsx"],
        file_name="express"
    ),
    "auto_fix": DownloadConfig(
        button_id="download-button-autofix",
        name="Auto Fix",
        requires_login=True,
        requires_checkboxes=True,
        download_patterns=["AutoFix*.xlsx"],
        file_name="autofix"
    ),
    "mundo_repcar": DownloadConfig(
        button_id="download-button-mundo-repcar",
        name="Mundo RepCar",
        requires_login=True,
        download_patterns=["MundoRepCar*.csv", "Lista_de_Precios*.csv"],
        file_name="repcar"
    )
}


class WebAutomationDownloader:
    """Clase para descargar archivos con una única sesión de navegador"""
    
    def __init__(self):
        """Inicializa el descargador de automatización web"""
        self.download_dir = os.path.join(os.getcwd(), "data_sin_procesar")
        self.screenshot_dir = os.path.join(self.download_dir, "screenshots")
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Configura el navegador y directorio de descargas"""
        # Crear directorios si no existen
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
            
        print(f"Directorio de descargas configurado: {self.download_dir}")
        print(f"Captura de pantalla habilitada: Las capturas se guardarán en {self.screenshot_dir}")
        
        # Configurar opciones de Chrome
        options = webdriver.ChromeOptions()
        
        # Opciones básicas
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=9222")
        
        # Opciones anti-detección
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        # User agent personalizado
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        options.add_argument(f'user-agent={user_agent}')
        
        # Configuración de descargas
        options.add_experimental_option("prefs", {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_settings.popups": 0
        })
        
        # Inicializar WebDriver
        self.driver = webdriver.Chrome(options=options)
        
        # Script para evadir detección
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                window.chrome = { runtime: {} };
                window.navigator.chrome = { runtime: {} };
            """
        })
        
        # Configurar wait
        self.wait = WebDriverWait(self.driver, 15)
        
    def _take_screenshot(self, service, step):
        """Toma una captura de pantalla para diagnóstico"""
        if not self.driver:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{service}_{step}-{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        try:
            self.driver.save_screenshot(filepath)
            print(f"Captura de pantalla guardada: {filepath}")
        except Exception as e:
            print(f"⚠️ Error al guardar captura: {str(e)}")
    
    def _perform_login(self):
        """Realiza el proceso de login"""
        try:
            print("Ingresando credenciales...")
            
            # Encontrar campo de usuario
            username_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_input.clear()
            username_input.send_keys(URL_USERNAME)
            print(f"Usuario ingresado: {URL_USERNAME}")
            
            # Encontrar campo de contraseña
            password_input = self.driver.find_element(By.ID, "password")
            password_input.clear()
            password_input.send_keys(URL_PASSWORD)
            print("Contraseña ingresada")
            
            # Hacer clic en el botón de "Iniciar sesión"
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button.login-button")
            print("🔓 Iniciando sesión...")
            login_button.click()
            
            # Esperar a que se complete el login
            self.wait.until(lambda driver: "login" not in driver.current_url)
            print("Login exitoso")
            
            return True
            
        except Exception as e:
            print(f"Error en el login: {e}")
            return False
    
    def _select_all_checkboxes(self):
        """Selecciona todos los checkboxes de marcas para Auto Fix"""
        try:
            print("📋 Seleccionando todas las marcas...")
            
            # Esperar a que aparezcan los checkboxes
            brands_container = self.wait.until(
                EC.presence_of_element_located((By.ID, "brands-checkboxes"))
            )
            print("  ✓ Contenedor de marcas encontrado")
            
            # Encontrar todos los checkboxes
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, "#brands-checkboxes input[type='checkbox']")
            print(f"  ✓ {len(checkboxes)} checkboxes detectados")
            
            # Marcar todos los checkboxes
            for i, checkbox in enumerate(checkboxes, 1):
                checkbox_id = checkbox.get_attribute("id")
                print(f"  ✓ Marcando checkbox {i}/{len(checkboxes)}: {checkbox_id}")
                
                if not checkbox.is_selected():
                    try:
                        checkbox.click()
                    except:
                        self.driver.execute_script("arguments[0].click();", checkbox)
            
            time.sleep(2)  # Dar tiempo a que se actualice la UI
            return True
            
        except Exception as e:
            print(f"Error seleccionando marcas: {e}")
            return False
    
    def _click_with_multiple_strategies(self, element, element_desc="botón"):
        """Intenta hacer clic en un elemento usando múltiples estrategias"""
        print("USANDO ESTRATEGIA MULTI-TÉCNICA")
        strategies = [
            ("click normal", lambda: element.click()),
            ("Actions API", lambda: ActionChains(self.driver).move_to_element(element).click().perform()),
            ("JavaScript", lambda: self.driver.execute_script("arguments[0].click();", element))
        ]
        
        for i, (name, func) in enumerate(strategies, 1):
            try:
                print(f"   {i}. Intentando {name}...")
                func()
                time.sleep(2)  # Esperar a que se procese el clic
                return True
            except Exception as e:
                pass
        
        print(f"Todas las estrategias de clic fallaron para {element_desc}")
        return False
    
    def _monitor_downloads(self, current_files: List[str], max_wait_time: int = 120) -> Optional[str]:
        """
        Monitorea el directorio de descargas para detectar nuevos archivos o archivos modificados
        
        Args:
            current_files: Lista de archivos actuales en el directorio
            max_wait_time: Tiempo máximo de espera en segundos
            
        Returns:
            Ruta al archivo descargado o None si no se detectó ninguno
        """
        print("⏳ Esperando descarga...")
        start_time = time.time()
        initial_check_time = time.time()
        
        # Patrones que coinciden con los archivos descargados para cada servicio
        # Esto nos ayudará a priorizar los archivos que coincidan con estos patrones
        download_patterns = []
        for config in DOWNLOAD_CONFIGS.values():
            if config.download_patterns:
                download_patterns.extend(config.download_patterns)
        
        # Guardar tiempos de modificación iniciales y tamaños
        initial_file_info = {}
        for file_path in current_files:
            try:
                initial_file_info[file_path] = {
                    'mtime': os.path.getmtime(file_path),
                    'size': os.path.getsize(file_path)
                }
            except Exception:
                initial_file_info[file_path] = {'mtime': 0, 'size': 0}
        
        # Función para detectar patrones
        def matches_pattern(filename, patterns):
            for pattern in patterns:
                if fnmatch.fnmatch(filename.lower(), pattern.lower()):
                    return True
            return False
        
        # Función para verificar archivos
        def check_for_new_files():
            all_files = glob.glob(os.path.join(self.download_dir, "*"))
            all_files = [f for f in all_files if not os.path.basename(f).startswith('.') and 
                        os.path.isfile(f) and not f.endswith('.tmp') and 
                        not f.endswith('.crdownload') and not f.endswith('.part') and
                        not os.path.basename(f).startswith('screenshot')]
            
            # Imprimir información de monitoreo
            elapsed = int(time.time() - start_time)
            print(f"⌛ Monitoreando directorio ({elapsed}s) - Archivos: {len(all_files)}")
            if all_files:
                print(f"📑 Archivos actuales: {', '.join(os.path.basename(f) for f in all_files)}")
            
            # Buscar archivos nuevos o modificados
            new_or_modified_files = []
            
            # 1. Verificar archivos nuevos
            new_files = [f for f in all_files if f not in current_files]
            if new_files:
                new_or_modified_files.extend(new_files)
                print(f"Archivo(s) nuevo(s) detectado(s): {', '.join(os.path.basename(f) for f in new_files)}")
            
            # 2. Verificar archivos existentes pero modificados
            for file_path in [f for f in all_files if f in current_files]:
                try:
                    current_mtime = os.path.getmtime(file_path)
                    current_size = os.path.getsize(file_path)
                    initial_mtime = initial_file_info.get(file_path, {}).get('mtime', 0)
                    initial_size = initial_file_info.get(file_path, {}).get('size', 0)
                    
                    # Si el archivo ha sido modificado o su tamaño ha cambiado
                    if current_mtime > initial_mtime or current_size != initial_size:
                        print(f"Archivo existente actualizado: {os.path.basename(file_path)}")
                        new_or_modified_files.append(file_path)
                except Exception:
                    pass
            
            # Si encontramos archivos nuevos o modificados
            if new_or_modified_files:
                # Primero, intentar encontrar archivos que coincidan con patrones conocidos
                pattern_matches = [f for f in new_or_modified_files 
                                if matches_pattern(os.path.basename(f), download_patterns)]
                
                if pattern_matches:
                    # Priorizar los archivos que coinciden con patrones conocidos
                    latest_file = max(pattern_matches, key=os.path.getmtime)
                else:
                    # Si no hay coincidencias, usar el archivo más reciente
                    latest_file = max(new_or_modified_files, key=os.path.getmtime)
                
                print(f"Archivo seleccionado para descarga: {os.path.basename(latest_file)}")
                return latest_file
            
            # Si no encontramos nada después de 30 segundos, buscar cualquier archivo que coincida con patrones
            if elapsed > 30 and not new_or_modified_files:
                pattern_matches = [f for f in all_files 
                                if matches_pattern(os.path.basename(f), download_patterns)]
                
                if pattern_matches:
                    print("⚠️ No se detectaron nuevos archivos, pero se encontró un archivo existente que coincide con el patrón esperado")
                    return max(pattern_matches, key=os.path.getmtime)
            
            return None
        
        # Verificación inmediata (a los 3 segundos)
        time.sleep(3)
        result = check_for_new_files()
        if result:
            return result
        
        # Bucle principal de monitoreo
        check_interval = 5  # Verificar cada 5 segundos
        last_check_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            # Verificar periódicamente
            if time.time() - last_check_time >= check_interval:
                result = check_for_new_files()
                if result:
                    return result
                last_check_time = time.time()
            
            # Si han pasado más de 45 segundos, asumir que la descarga ya ocurrió
            # y buscar un archivo que coincida con los patrones esperados
            if time.time() - start_time > 45:
                all_files = glob.glob(os.path.join(self.download_dir, "*"))
                all_files = [f for f in all_files if not os.path.basename(f).startswith('.') and 
                            os.path.isfile(f) and not f.endswith('.tmp') and 
                            not f.endswith('.crdownload') and not f.endswith('.part') and
                            not os.path.basename(f).startswith('screenshot')]
                
                pattern_matches = [f for f in all_files 
                                if matches_pattern(os.path.basename(f), download_patterns)]
                
                if pattern_matches:
                    best_match = max(pattern_matches, key=os.path.getmtime)
                    print(f"⏱️ Se alcanzó el tiempo de espera máximo (45s), usando archivo existente que coincide con el patrón: {os.path.basename(best_match)}")
                    return best_match
                elif all_files:
                    # Si no hay coincidencias pero hay archivos, usar el más reciente
                    most_recent_file = max(all_files, key=os.path.getmtime)
                    print(f"⏱️ Se alcanzó el tiempo de espera máximo (45s), usando el archivo más reciente: {os.path.basename(most_recent_file)}")
                    return most_recent_file
                    
                print(f"⏱️ Se alcanzó el tiempo de espera máximo (45s), continuando con el siguiente servicio")
                return None
                
            time.sleep(0.5)
        
        # Si llegamos aquí, se agotó el tiempo de espera
        print(f"⚠️ Timeout alcanzado para descarga")
        
        # Verificación final
        result = check_for_new_files()
        if result:
            return result
            
        print("FALLÓ: No se detectó un nuevo archivo")
        return None
            
    def _download_auto_express(self) -> Optional[str]:
        """
        Descarga desde Autorepuestos Express
        """
        try:
            print("\n📂 1/3: DESCARGANDO AUTOREPUESTOS EXPRESS...")
            
            # Navegar a la página principal
            print("🌐 Navegando a la página principal...")
            self.driver.get(URL_PAGE)
            time.sleep(2)
            
            # Buscar y hacer clic en el botón
            print("🔍 Buscando botón de Autorepuestos Express...")
            
            auto_express_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, DOWNLOAD_CONFIGS["auto_express"].button_id))
            )
            
            print("🖱️  Haciendo clic en el botón...")
            self._click_with_multiple_strategies(auto_express_button, "botón de Auto Express")
            
            # Esperar descarga
            current_files = glob.glob(os.path.join(self.download_dir, "*"))
            current_files = [f for f in current_files if not os.path.basename(f).startswith('.') and 
                            os.path.isfile(f) and not f.endswith('.tmp') and 
                            not f.endswith('.crdownload') and not f.endswith('.part') and
                            not os.path.basename(f).startswith('screenshot')]
            
            if current_files:
                print(f"ℹ️ Se encontraron {len(current_files)} archivos existentes antes de la descarga:")
                for idx, file in enumerate(current_files, 1):
                    print(f"  {idx}. {os.path.basename(file)}")
            
            # Usar un tiempo máximo de espera más corto para este servicio (60 segundos)
            downloaded_file = self._monitor_downloads(current_files, 60)
            
            if downloaded_file:
                # Renombrar el archivo usando el file_name configurado
                file_ext = os.path.splitext(downloaded_file)[1]  # Obtener la extensión
                new_filename = DOWNLOAD_CONFIGS["auto_express"].file_name + file_ext
                new_filepath = os.path.join(self.download_dir, new_filename)
                
                try:
                    if os.path.exists(new_filepath):
                        os.remove(new_filepath)  # Eliminar archivo existente con mismo nombre
                    
                    os.rename(downloaded_file, new_filepath)
                    print(f"Archivo renombrado: {os.path.basename(downloaded_file)} → {new_filename}")
                    downloaded_file = new_filepath
                except Exception as e:
                    print(f"⚠️ No se pudo renombrar el archivo: {str(e)}")
                
                print(f"🎉 ÉXITO: Descarga completada para Autorepuestos Express")
                print(f"📁 Archivo: {os.path.basename(downloaded_file)} ({os.path.getsize(downloaded_file):,} bytes)")
            
            return downloaded_file
            
        except Exception as e:
            print(f"💥 Error en descarga de Auto Express: {str(e)}")
            return None
    
    def _download_auto_fix(self) -> Optional[str]:
        """
        Descarga desde Auto Fix
        """
        try:
            print("\n📂 2/3: DESCARGANDO AUTO FIX...")
            
            # Volver a la página principal
            print("🔙 Volviendo a la página principal...")
            self.driver.get(URL_PAGE)
            time.sleep(2)
            
            # Buscar y hacer clic en el botón
            print("🔍 Buscando botón de Auto Fix...")
            # self._take_screenshot("auto_fix", "1-pagina_principal")
            
            auto_fix_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, DOWNLOAD_CONFIGS["auto_fix"].button_id))
            )
            
            print("🖱️  Haciendo clic en el botón...")
            auto_fix_button.click()
            
            # Verificar si requiere login
            if "login" in self.driver.current_url:
                print("🔐 Detectada redirección a página de login")
                # self._take_screenshot("auto_fix", "2-login")
                
                if not self._perform_login():
                    return None
            
            # Seleccionar todas las marcas
            # self._take_screenshot("auto_fix", "3-seleccion_marcas")
            if not self._select_all_checkboxes():
                return None
            
            # Buscar el botón de descarga
            print("🔍 Buscando botón de descarga...")
            # self._take_screenshot("auto_fix", "4-boton_descarga")
            
            download_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Descargar lista de precios')]"))
            )
            
            print("🖱️  Haciendo clic en el botón...")
            self._click_with_multiple_strategies(download_button, "botón de descarga")
            
            # Esperar a que se complete la descarga
            current_files = glob.glob(os.path.join(self.download_dir, "*"))
            current_files = [f for f in current_files if not os.path.basename(f).startswith('.') and 
                            os.path.isfile(f) and not f.endswith('.tmp') and 
                            not f.endswith('.crdownload') and not f.endswith('.part') and
                            not os.path.basename(f).startswith('screenshot')]
            
            downloaded_file = self._monitor_downloads(current_files)
            
            if downloaded_file:
                # Renombrar el archivo usando el file_name configurado
                file_ext = os.path.splitext(downloaded_file)[1]  # Obtener la extensión
                new_filename = DOWNLOAD_CONFIGS["auto_fix"].file_name + file_ext
                new_filepath = os.path.join(self.download_dir, new_filename)
                
                try:
                    if os.path.exists(new_filepath):
                        os.remove(new_filepath)  # Eliminar archivo existente con mismo nombre
                    
                    os.rename(downloaded_file, new_filepath)
                    print(f"Archivo renombrado: {os.path.basename(downloaded_file)} → {new_filename}")
                    downloaded_file = new_filepath
                except Exception as e:
                    print(f"⚠️ No se pudo renombrar el archivo: {str(e)}")
                
                print(f"🎉 ÉXITO: Descarga completada para Auto Fix")
                print(f"📁 Archivo: {os.path.basename(downloaded_file)} ({os.path.getsize(downloaded_file):,} bytes)")
            
            return downloaded_file
            
        except Exception as e:
            print(f"💥 Error en descarga de Auto Fix: {str(e)}")
            return None
    
    def _download_mundo_repcar(self) -> Optional[str]:
        """
        Descarga desde Mundo RepCar
        """
        try:
            print("\n📂 3/3: DESCARGANDO MUNDO REPCAR...")
            
            # Volver a la página principal
            print("🔙 Volviendo a la página principal...")
            self.driver.get(URL_PAGE)
            time.sleep(2)
            
            # Buscar y hacer clic en el botón
            print("🔍 Buscando botón de Mundo RepCar...")
            # self._take_screenshot("mundo_repcar", "1-pagina_principal")
            
            mundo_repcar_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, DOWNLOAD_CONFIGS["mundo_repcar"].button_id))
            )
            
            print("🖱️  Haciendo clic en el botón...")
            mundo_repcar_button.click()
            
            # Verificar si requiere login
            if "login" in self.driver.current_url:
                print("🔐 Detectada redirección a página de login")
                # Si ya hicimos login antes, no será necesario volver a hacer login
                if "username" in self.driver.page_source:
                    print("Ingresando credenciales...")
                    if not self._perform_login():
                        return None
                else:
                    print("Usando sesión existente...")
                    print("Login exitoso")
            
            # Buscar botón de descarga
            print("🔍 Buscando botón de descarga...")
            # self._take_screenshot("mundo_repcar", "2-pagina_descarga")
            
            # Buscar utilizando diferentes selectores
            selectors = [
                (By.CSS_SELECTOR, "button.download-button"),
                (By.XPATH, "//button[contains(text(), 'Descargar')]"),
                (By.XPATH, "//a[contains(@class, 'download')]")
            ]
            
            download_element = None
            for selector_type, selector in selectors:
                try:
                    elements = self.driver.find_elements(selector_type, selector)
                    if elements:
                        download_element = elements[0]
                        print(f"Botón encontrado con selector: {selector}")
                        break
                except:
                    pass
            
            if not download_element:
                print("No se encontró el botón de descarga")
                return None
            
            # Analizar el elemento para ver si tiene un enlace
            print("🔎 Analizando elemento:")
            element_tag = download_element.tag_name
            element_class = download_element.get_attribute("class")
            print(f"  • Tipo: {element_tag}")
            print(f"  • Clase: {element_class}")
            
            # Hacer clic en el botón normalmente
            print("🖱️  Haciendo clic en el botón...")
            self._click_with_multiple_strategies(download_element, "botón de descarga")
            
            # Esperar a que se complete la descarga
            current_files = glob.glob(os.path.join(self.download_dir, "*"))
            current_files = [f for f in current_files if not os.path.basename(f).startswith('.') and 
                            os.path.isfile(f) and not f.endswith('.tmp') and 
                            not f.endswith('.crdownload') and not f.endswith('.part') and
                            not os.path.basename(f).startswith('screenshot')]
            
            downloaded_file = self._monitor_downloads(current_files)
            
            if downloaded_file:
                # Renombrar el archivo usando el file_name configurado
                file_ext = os.path.splitext(downloaded_file)[1]  # Obtener la extensión
                new_filename = DOWNLOAD_CONFIGS["mundo_repcar"].file_name + file_ext
                new_filepath = os.path.join(self.download_dir, new_filename)
                
                try:
                    if os.path.exists(new_filepath):
                        os.remove(new_filepath)  # Eliminar archivo existente con mismo nombre
                    
                    os.rename(downloaded_file, new_filepath)
                    print(f"Archivo renombrado: {os.path.basename(downloaded_file)} → {new_filename}")
                    downloaded_file = new_filepath
                except Exception as e:
                    print(f"⚠️ No se pudo renombrar el archivo: {str(e)}")
                
                print(f"🎉 ÉXITO: Descarga completada para Mundo RepCar")
                print(f"📁 Archivo: {os.path.basename(downloaded_file)} ({os.path.getsize(downloaded_file):,} bytes)")
            
            return downloaded_file
            
        except Exception as e:
            print(f"💥 Error en descarga de Mundo RepCar: {str(e)}")
            return None

def download_all_files_single_session(services_to_download: List[str] = None, max_wait_time: int = 120, clean_download_dir: bool = False) -> Dict[str, Optional[str]]:
  
    # Si no se especifican servicios, usar todos
    if services_to_download is None:
        services_to_download = ["auto_express", "auto_fix", "mundo_repcar"]
    
    # Crear una instancia única del downloader
    downloader = WebAutomationDownloader()
    results = {}
    
    try:

        print("Servicios: Autorepuestos Express, Auto Fix y Mundo RepCar")
        print("============================================================")
        print("🚀 INICIANDO AUTOMATIZACIÓN CON SESIÓN ÚNICA")
        print("============================================================\n")
        
        # Inicializar navegador una sola vez
        print("⚙️  Configurando navegador único para todas las descargas...")
        downloader.setup_driver()
        print("Navegador iniciado exitosamente\n")
        
        # Limpiar directorio de descargas si se solicita
        if clean_download_dir:
            download_dir = downloader.download_dir
            try:
                print("🧹 Limpiando directorio de descargas...")
                files_to_delete = glob.glob(os.path.join(download_dir, "*"))
                files_to_delete = [f for f in files_to_delete if not os.path.basename(f).startswith('.') and 
                                os.path.isfile(f) and not os.path.basename(f).startswith('screenshot')]
                
                for file_path in files_to_delete:
                    try:
                        os.remove(file_path)
                        print(f"  ✓ Eliminado: {os.path.basename(file_path)}")
                    except Exception as e:
                        print(f"  ✗ No se pudo eliminar {os.path.basename(file_path)}: {str(e)}")
                
                print(f"Se eliminaron {len(files_to_delete)} archivos del directorio de descargas")
            except Exception as e:
                print(f"⚠️ Error al limpiar directorio de descargas: {str(e)}")
        
        # Medir el tiempo total
        start_time = time.time()
        
        # Descargar cada servicio secuencialmente
        for service in services_to_download:
            # Descargar el archivo según el servicio
            if service == "auto_express":
                file_path = downloader._download_auto_express()
            elif service == "auto_fix":
                file_path = downloader._download_auto_fix()
            elif service == "mundo_repcar":
                file_path = downloader._download_mundo_repcar()
            else:
                continue
                
            # Guardar resultado
            results[service] = file_path
        
        # Calcular tiempo total
        total_time = time.time() - start_time
        
        # Mostrar resumen
        print("\n============================================================")
        print("📊 RESUMEN DE DESCARGAS (SESIÓN ÚNICA):")
        print("============================================================")
        
        successful_count = 0
        for service, file_path in results.items():
            # Obtener el nombre configurado y el nombre mostrado
            config_name = DOWNLOAD_CONFIGS[service].name
            file_name_config = DOWNLOAD_CONFIGS[service].file_name
            
            if file_path:
                file_size = os.path.getsize(file_path)
                file_name = os.path.basename(file_path)
                print(f"{config_name.ljust(20)} - {file_name} ({file_size:,} bytes)")
                successful_count += 1
            else:
                print(f"{config_name.ljust(20)} - DESCARGA FALLIDA")
        
        # Mostrar resultado final
        if successful_count == len(services_to_download):
            print(f"\n🎉 ¡ÉXITO TOTAL! {successful_count}/{len(services_to_download)} descargas completadas correctamente")
        else:
            print(f"\n🏁 RESULTADO FINAL: {successful_count}/{len(services_to_download)} descargas exitosas")
        
        print(f"⏱️  Tiempo total de proceso: {total_time:.2f} segundos")
        print("============================================================")
        
        return results
    
    except Exception as e:
        print(f"💥 Error general en la automatización: {str(e)}")
        return {}
    
    finally:
        # Cerrar el navegador al finalizar todas las descargas
        if downloader.driver:
            print("🔒 Cerrando navegador...")
            try:
                downloader.driver.quit()
                print("Navegador cerrado correctamente")
            except Exception as e:
                print(f"⚠️ Error al cerrar navegador: {str(e)}")
                
        # Mostrar información final
        print("\n🎊 PROCESO COMPLETADO:")
        successful_downloads = {k: v for k, v in results.items() if v is not None}
        failed_downloads = {k: v for k, v in results.items() if v is None}
        
        print(f"Exitosos: {len(successful_downloads)}")
        print(f"Fallidos: {len(failed_downloads)}")
        
        if successful_downloads:
            print("\n📦 ARCHIVOS DESCARGADOS:")
            for service, file_path in successful_downloads.items():
                print(f"   • {service}: {file_path}")
        
        if failed_downloads:
            print("\n⚠️  DESCARGAS FALLIDAS:")
            for service in failed_downloads:
                print(f"   • {service}")