from datetime import datetime
from getpass import getpass
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from zoneinfo import ZoneInfo
import time


def find_element(
    driver: webdriver,
    by: str,
    path: str,
    timeout: int = 3,
) -> webelement:
    try:
        element = driver.find_element(by, path)
    except:
        time.sleep(timeout)
        element = driver.find_element(by, path)

    return element


def get_conference_cfp(
    driver: webdriver,
    conference: dict[str, str],
    name: str,
) -> None:
    url   = conference["url"]
    xpath = conference["xpath"]
    fmt   = conference["fmt"]
    zones = conference["zones"]

    driver.get(url)
    cfp = find_element(driver, By.XPATH, xpath).text.rstrip()

    print("[{n:>15}]".format(n=name), end=" ")
    try:
        cfp, zone = cfp, ""
        for i in range(zones):
            cfp, zone = cfp.rsplit(" ", 1)
        print(datetime.strptime(cfp, fmt))
    except:
        print(cfp)


if __name__ == "__main__":
    conferences = {
        "NIPS": {
            "url"  : "https://neurips.cc/Conferences/2024",
            "xpath": "/html/body/main/div[2]/div/div/div[7]/table[2]/tbody/tr[4]/td[2]/span[1]",
            "fmt"  : "%B %d '%y %I:%M %p",
            "zones": 1,
        },
        "EuroSys Spring": {
            "url"  : "https://2025.eurosys.org",
            "xpath": "/html/body/section/div/div/div/ul[1]/li[2]/strong",
            "fmt"  : "%A, %B %d, %Y",
            "zones": 1,
        },
        "EuroSys Fall": {
            "url"  : "https://2025.eurosys.org",
            "xpath": "/html/body/section/div/div/div/ul[2]/li[2]/strong",
            "fmt"  : "%A, %B %d, %Y",
            "zones": 1,
        },
        "HPDC": {
            "url"  : "https://www.hpdc.org/2024/calls-cfp.html",
            "xpath": "/html/body/div/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/ul/li[1]/del/p/strong",
            "fmt"  : "%B %d, %Y.",
            "zones": 0,
        },
        "OSDI": {
            "url"  : "https://www.usenix.org/conference/osdi25/call-for-papers",
            "xpath": "/html/body/div[2]/main/section/div[3]/article/div/div/div/div/div[1]/div/div/div/div/div/div" +
                     "/div/div/div/div/div/div/ul[1]/li[2]/strong",
            "fmt"  : "%A, %B %d, %Y, %H:%M %p",
            "zones": 4,
        },
        "PACT": {
            "url"  : "https://pact2024.github.io",
            "xpath": "/html/body/div/div/div[2]/ul[1]/li[2]",
            "fmt"  : "%A, %B %d, %Y, %H:%M %p",
            "zones": 0,
        },
    }

    with Display(visible=False, size=(1200,1200)):
        """ set up firefox.service """
        service = webdriver.firefox.service.Service()
        service.path = "/usr/bin/geckodriver"

        """ set up firefox.options """
        options = webdriver.firefox.options.Options()
        options.headless = True

        """ initialize driver """
        browser = webdriver.Firefox(service=service, options=options)

        for name in conferences.keys():
            get_conference_cfp(browser, conferences[name], name)

        browser.close()
