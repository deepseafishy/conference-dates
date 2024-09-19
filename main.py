from datetime import datetime
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import multiprocessing as mp
import time


def find_element(
    driver: webdriver,
    by: str,
    path: str,
    timeout: int = 1,
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
) -> str:
    url   = conference["url"]
    xpath = conference["xpath"]
    fmt   = conference["fmt"]
    zones = conference["zones"]

    """ access URL """
    driver.get(url)

    """ retrieve CfP information """
    cfp = find_element(driver, By.XPATH, xpath).text.split()

    """ format string """
    result = "[{n:>15}] ".format(n=name)
    try:
        cfp = ' '.join(cfp[:len(cfp) - zones])
        result += str(datetime.strptime(cfp, fmt))
    except:
        result += cfp

    return result


def main(information) -> str:
    conference = information[0]
    name       = information[1]
    # print("Getting {n}...".format(n=name))

    with Display(visible=False, size=(10,10)):
        """ set up firefox.service """
        service = webdriver.firefox.service.Service()
        service.path = "/usr/bin/geckodriver"

        """ set up firefox.options """
        options = webdriver.firefox.options.Options()
        options.headless = True

        """ initialize driver """
        browser = webdriver.Firefox(service=service, options=options)

        """ crawl CfP information """
        result = get_conference_cfp(browser, conference, name)
        browser.close()

    return result


if __name__ == "__main__":
    conferences = {
        "ICML": {
            "url"  : "https://icml.cc/Conferences/2024/Dates",
            "xpath": "/html/body/main/div[2]/div/div/div[3]/table/tbody/tr[13]/td[3]/span",
            "fmt"  : "%b %d '%y",
            "zones": 3,
        },
        "NIPS": {
            "url"  : "https://neurips.cc/Conferences/2024",
            "xpath": "/html/body/main/div[2]/div/div/div[7]/table[2]/tbody/tr[4]/td[2]/span[1]",
            "fmt"  : "%B %d '%y %I:%M %p",
            "zones": 1,
        },
        "Spring EuroSys": {
            "url"  : "https://2025.eurosys.org",
            "xpath": "/html/body/section/div/div/div/ul[1]/li[2]/strong",
            "fmt"  : "%A, %B %d, %Y",
            "zones": 1,
        },
        "Fall EuroSys": {
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
        "PPoPP": {
            "url"  : "https://ppopp25.sigplan.org",
            "xpath": "/html/body/div/div[3]/div[1]/div[2]/div[2]/table/tbody/tr[3]/td",
            "fmt"  : "%a %d %b %Y",
            "zones": 5,
        },
    }

    results = mp.Pool().map(main, zip(conferences.values(), conferences.keys()))
    print('\n'.join(results))
