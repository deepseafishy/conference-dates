from datetime import datetime, timedelta, timezone
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from zoneinfo import ZoneInfo
import multiprocessing as mp
import time
import os
import re


def remove_ordinal_suffix(date: str) -> str:
    return re.sub("TH|ST|ND|RD", '', date)


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
    zones: dict[str, str],
    conference: dict[str, str],
    name: str,
) -> str:
    url   = conference["url"]
    xpath = conference["xpath"]
    fmt   = conference["fmt"]
    result = "[{n:>15}] ".format(n=name)
    default_time = datetime(1900, 1, 2, 0, 0).astimezone(zones["KST"])

    """ access URL """
    try:
        driver.get(url)
    except:
        return result + "Failed URL", None, default_time

    """ retrieve CfP information """
    try:
        cfp = find_element(driver, By.XPATH, xpath).text.upper()
        cfp = remove_ordinal_suffix(cfp).split()
    except:
        return result + "Failed XPath", None, default_time

    """ find timezone """
    zone = ""
    for substring in cfp:
        zone = substring if substring in zones.keys() else zone

    """ format string """
    fmt_len, cfp_len = len(fmt.split()), len(cfp)
    time = ' '.join(cfp)
    for i in range(cfp_len - fmt_len + 1):
        try:
            time = datetime.strptime(' '.join(cfp[i:i + fmt_len]), fmt)
        except:
            pass

    """ check if parsing failed """
    if not isinstance(time, datetime):
        result += time
        return result, None, default_time

    """ apply timezone """
    if zone == "":
        """ apply AoE if no timezone is specified """
        time += timedelta(hours=36)
        time = time.replace(tzinfo=timezone.utc)
        """ apply KST """
        time = time.astimezone(zones["KST"])
        result += time.strftime("%Y %b %d, %H:%M")
    else:
        """ apply timezone if specified """
        time = time.replace(tzinfo=zones[zone])
        """ apply KST """
        time = time.astimezone(zones["KST"])
        result += time.strftime("%Y %b %d, %H:%M")

    return result, time, time.replace(year=1900)


def main(
    conferences: dict[str, dict[str, str]],
    name: str,
    queue: mp.Queue,
) -> None:
    zones = {
        "PDT" : ZoneInfo("America/Los_Angeles"),
        "PST" : ZoneInfo("America/Los_Angeles"),
        "CET" : ZoneInfo("Europe/Berlin"),
        "CEST": ZoneInfo("Europe/Berlin"),
        "EST" : ZoneInfo("America/New_York"), # UTC-5
        "KST" : ZoneInfo("Asia/Seoul"),
    }

    with Display(visible=False):
        """ set up firefox.service """
        service = webdriver.firefox.service.Service()
        service.path = "/usr/bin/geckodriver"

        """ set up firefox.options """
        options = webdriver.firefox.options.Options()
        options.headless = True

        """ initialize driver """
        browser = webdriver.Firefox(service=service, options=options)

        """ crawl CfP information """
        result, time_real, time_1900 = get_conference_cfp(browser, zones, conferences[name], name)
        browser.close()

    """ append retrieved results to the queue """
    queue.put([name, result, time_real, time_1900])

    return


if __name__ == "__main__":
    conferences = {
        "DAC": {
            "url"  : "https://www.dac.com/Conference/2025-Call-for-Contributions",
            "xpath": "/html/body/form/main/div[1]/div/div/div[2]/div/div/div/div/div/div/ul[1]/li[2]",
            "fmt"  : "%B %d, %Y %I:%M %p",
        },
        "DATE": {
            "url"  : "https://www.date-conference.com/call-for-papers",
            "xpath": "/html/body/div/main/div/div[3]/article/div/div[1]/table[1]/tbody/tr[3]/td[2]/b",
            "fmt"  : "%A, %d %B %Y",
        },
        "ICML": {
            "url"  : "https://icml.cc/Conferences/2024/Dates",
            "xpath": "/html/body/main/div[2]/div/div/div[3]/table/tbody/tr[13]/td[3]/span",
            "fmt"  : "%b %d '%y",
        },
        "NIPS": {
            "url"  : "https://neurips.cc/Conferences/2024",
            "xpath": "/html/body/main/div[2]/div/div/div[7]/table[2]/tbody/tr[4]/td[2]/span[1]",
            "fmt"  : "%b %d '%y",
        },
        "Spring EuroSys": {
            "url"  : "https://2025.eurosys.org",
            "xpath": "/html/body/section/div/div/div/ul[1]/li[2]/strong",
            "fmt"  : "%A, %B %d, %Y",
        },
        "Fall EuroSys": {
            "url"  : "https://2025.eurosys.org",
            "xpath": "/html/body/section/div/div/div/ul[2]/li[2]/strong",
            "fmt"  : "%A, %B %d, %Y",
        },
        "HPDC": {
            "url"  : "https://www.hpdc.org/2024/calls-cfp.html",
            "xpath": "/html/body/div/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/ul/li[1]/del/p/strong",
            "fmt"  : "%B %d, %Y.",
        },
        "OSDI": {
            "url"  : "https://www.usenix.org/conference/osdi25/call-for-papers",
            "xpath": "/html/body/div[2]/main/section/div[3]/article/div/div/div/div/div[1]/div/div/div/div/div/div" +
                     "/div/div/div/div/div/div/ul[1]/li[2]/strong",
            "fmt"  : "%A, %B %d, %Y, %I:%M %p",
        },
        "PACT": {
            "url"  : "https://pact2024.github.io",
            "xpath": "/html/body/div/div/div[2]/ul[1]/li[2]",
            "fmt"  : "%B %d, %Y",
        },
        "PPoPP": {
            "url"  : "https://ppopp25.sigplan.org/dates",
            "xpath": "/html/body/div/div[3]/div[2]/div/table/tbody/tr[4]/td[1]",
            "fmt"  : "%a %d %b %Y",
        },
        "FAST": {
            "url"  : "https://www.usenix.org/conference/fast25/call-for-papers",
            "xpath": "/html/body/div[2]/main/section/div[3]/article/div/div/div/div/div[1]/div/div/div/div/div/div" +
                     "/div/div/div/div/div/div/ul[1]/li[1]/strong",
            "fmt"  : "%A, %B %d, %Y, %I:%M %p",
        },
        "ATC": {
            "url"  : "https://www.usenix.org/conference/atc25/call-for-papers",
            "xpath": "/html/body/div[2]/main/section/div[3]/article/div/div/div/div/div[1]/div/div/div/div/div/div" +
                     "/div/div/div/div/div/div/ul/li[2]/strong",
            "fmt"  : "%A, %B %d, %Y, %I:%M %p",
        },
        "APSys": {
            "url"  : "https://ap-sys.org",
            "xpath": "/html/body/main/div/div[2]/div[2]/div[2]/div/aside/p[3]/b",
            "fmt"  : "%B %d, %Y",
        },
        "Spring ASPLOS": {
            "url"  : "https://www.asplos-conference.org/asplos2025/cfp",
            "xpath": "/html/body/div/div/div/div/div/main/article/div/ul[1]/li[2]",
            "fmt"  : "%B %d, %Y",
        },
        "Summer ASPLOS": {
            "url"  : "https://www.asplos-conference.org/asplos2025/cfp",
            "xpath": "/html/body/div/div/div/div/div/main/article/div/ul[2]/li[2]",
            "fmt"  : "%B %d, %Y",
        },
        "Fall ASPLOS": {
            "url"  : "https://www.asplos-conference.org/asplos2025/cfp",
            "xpath": "/html/body/div/div/div/div/div/main/article/div/ul[3]/li[1]",
            "fmt"  : "%B %d, %Y",
        },
        "SPAA": {
            "url"  : "https://spaa.acm.org/call-for-papers/",
            "xpath": "/html/body/div/div/div/main/article/div/figure/table/tbody/tr[2]/td[2]",
            "fmt"  : "%B %d, %Y %H:%M%p"
        },
        "EuroPar": {
            "url"  : "https://2024.euro-par.org/calls/papers/",
            "xpath": "/html/body/div[1]/div[2]/div[4]/div/div/div/div/div/div[1]/div/div/div/div/table/tbody/tr[2]/" +
                     "td[2]/strong/span[1]",
            "fmt"  : "%B %d, %Y",
        },
        "INFOCOM": {
            "url"  : "https://infocom2025.ieee-infocom.org",
            "xpath": "/html/body/div[6]/div/div/div[2]/aside/div/section/p[2]/span[2]",
            "fmt"  : "%A, %d %B %Y (%H:%M%p"
        },
    }

    """ print saved CfP dates """
    if os.path.isfile("./cfp_dates.txt"):
        print("\nSAVED RESULTS")
        with open("./cfp_dates.txt", 'r') as infile:
            for line in infile:
                data = line.split(',')
                result = "[{n:>15}] ".format(n=data[0])

                if data[1] != "None":
                    data[1] = datetime.strptime(data[1], "%Y-%m-%d %H:%M:%S%z")
                    data[1] = data[1].strftime("%Y %b %d, %H:%M")
                result += data[1]
                print(result)
    print()

    """ spawn processes for simulatneous CfP date retrievals """
    mp.set_start_method("spawn")
    queue = mp.Queue()
    for key in conferences.keys():
        mp.Process(target=main, args=(conferences, key, queue,)).start()

    results = []
    progress = ["\r",] + ["." for _ in range(len(conferences.keys()))]
    for i in range(len(conferences.keys()) + 1):
        if i < len(conferences.keys()):
            """ update the progress bar """
            print(''.join(progress), end='', flush=True)
            name, result, time_real, time_1900 = queue.get()
            results.append([name, result, time_real, time_1900, conferences[name]["url"]])
            progress[list(conferences.keys()).index(name) + 1] = "o"
        else:
            """ clear the progress bar """
            print('\r', end='', flush=True)

    """ print retrieved CfP dates in sorted order """
    results = sorted(results, key=lambda x: x[3])
    print("RETRIEVED RESULTS")
    print('\n'.join(f"{result[1]} ({result[-1]})" for result in results))

    """ save retrieved CfP dates into a file """
    with open("./cfp_dates.txt", 'w+') as outfile:
        for result in results:
            key_value = [result[0], str(result[2]), '\n']
            outfile.write(','.join(key_value))
