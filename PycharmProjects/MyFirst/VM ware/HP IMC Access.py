from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def auto_login():
    url = "http://10.222.1.123:8080/"
    username = "admin"
    password = "Armin@2512"

    options = Options()
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        wait = WebDriverWait(driver, 15)

        username_field = wait.until(
            EC.element_to_be_clickable((By.ID, "loginForm:loginName"))
        )
        username_field.click()
        username_field.send_keys(username)

        password_field = wait.until(
            EC.element_to_be_clickable((By.ID, "loginForm:password"))
        )
        password_field.click()
        password_field.send_keys(password)

        login_button = wait.until(
            EC.element_to_be_clickable((By.ID, "loginForm:loginCmd"))
        )
        login_button.click()

        print("Login successful - browser will stay open")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    auto_login()
