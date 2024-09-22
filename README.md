# Conference Dates

A Python Selenium crawler for various conference CfP dates.
Everything is hardcoded, so just run the script.

## Prerequisite

 - This code requires `pyvirtualdisplay` and `selenium`.
    ```bash
    pip install pyvirtualdisplay selenium
    ```
 - `pyvirtualdisplay` requires `xvfb` package installed.
    ```bash
    sudo apt-get install xvfb
    ```

## Usage

```bash
python3 main.py
```

## TODO
- [x] Create multiple processes to gather information faster
- [x] Apply time zones
- [x] Sort conferences by the dates
- [ ] Add debug option
- [ ] Automatically find CfP dates
- [ ] Automatically look for extended CfP dates
- [ ] Automatically renew conferences yearly
  - [ ] Add conference dates
  - [ ] Renew conferences after conference dates pass
  - [ ] Show previous conference dates if the new conference site doesn't exist
