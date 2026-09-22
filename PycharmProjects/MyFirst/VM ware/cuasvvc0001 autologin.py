from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def auto_login():
    url = "https://cuasvvc0001.ua.inpkg.net/ui/"
    username = "administrator@vsphere.local"
    password = "VerAl1i@admin"

    options = Options()
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.send_keys(username)

        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "submit").click()

        print("Login successful - browser will stay open")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    auto_login()