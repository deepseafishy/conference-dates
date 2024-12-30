# Conference Dates

A Python Selenium crawler for various conference CfP dates.
This script looks for preprocessed conference information in `conferences.txt` to know which information to crawl for.

## Prerequisite

 - This code requires `pyvirtualdisplay` and `selenium`.
    ```bash
    pip install pyvirtualdisplay selenium
    ```
 - `pyvirtualdisplay` requires `xvfb` package installed.
    ```bash
    sudo apt-get install xvfb
    ```
 - Preprocessed information in `conferences.txt`
    - This script requires four information: conference name, URL, XPath for the CfP date, and the given date format.
    - These information must be stored in order in each line and an additional empty line for readability, i.e., a total of five lines is required per conference.
    - Below is an example text of information about two conferences.
    ```
    FAST
    https://www.usenix.org/conference/fast25/call-for-papers
    /html/body/div[2]/main/section/div[3]/article/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/ul[1]/li[1]/strong
    %A, %B %d, %Y, %I:%M %p

    ATC
    https://www.usenix.org/conference/atc25/call-for-papers
    /html/body/div[2]/main/section/div[3]/article/div/div/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/ul/li[2]/strong
    %A, %B %d, %Y, %I:%M %p


    ```

## Usage

```bash
python3 main.py
```

## TODO
- [x] Create multiple processes to gather information faster
- [x] Apply time zones
- [x] Sort conferences by the dates
- [ ] Add author notification dates
- [ ] Automatically find CfP dates
- [ ] Automatically look for extended CfP dates
- [ ] Automatically renew conferences yearly
  - [ ] Add conference dates
  - [ ] Renew conferences after conference dates pass
  - [ ] Show previous conference dates if the new conference site doesn't exist
