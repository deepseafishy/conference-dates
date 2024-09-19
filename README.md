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
- [ ] Create multiple processes to gather information faster
- [ ] Sort conferences by the dates
- [ ] Automatically renew conferences yearly
