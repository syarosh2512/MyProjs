import traceback

from selenium import webdriver
from selenium.common.exceptions import InvalidSessionIdException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def auto_login():
    host = "10.222.1.220"
    password = "19815102"
    url = f"http://{host}/login.ssi"

    options = Options()
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Корпоративна GPO примусово ставить розширення (ExtensionInstallForcelist,
    # у chrome://policy позначено "Warning, Conflict"). На кожному новому
    # тимчасовому профілі Chrome намагається довстановити це розширення
    # заново при старті - саме це може бути причиною нестабільних падінь.
    # Прибираємо розширення з автоматизованої сесії, щоб перевірити гіпотезу.
    options.add_argument("--disable-extensions")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("detach", True)

    # Пишемо verbose-лог chromedriver у файл поруч зі скриптом, щоб при
    # наступному падінні побачити РЕАЛЬНУ причину (а не здогадку), як і
    # радить саме повідомлення selenium: "Examine ChromeDriver verbose log".
    service = Service(
        log_output="chromedriver.log",
        service_args=["--verbose"],
    )

    try:
        driver = webdriver.Chrome(options=options, service=service)
        driver.get(url)

        wait = WebDriverWait(driver, 15)

        account_select = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "select"))
        )
        Select(account_select).select_by_visible_text("Administrator")

        password_field = wait.until(
            EC.element_to_be_clickable((By.ID, "password"))
        )
        password_field.click()
        password_field.send_keys(password)
        password_field.submit()

        print("Login submitted - browser will stay open")

    except (InvalidSessionIdException, WebDriverException) as e:
        print(
            "Error: Chrome closed/crashed mid-run, or a step failed. "
            "Full details below and in chromedriver.log.\n"
            f"Details: {e}"
        )
        traceback.print_exc()
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    auto_login()
