# colorlog

## example

```python
from colorlog import logging

logging.basicConfig(level=logging.DEBUG)

logging.debug("jawide")
logging.info("jawide")
logging.warning("jawide")
logging.error("jawide")
logging.critical("jawide")
```

## setup

```bash
pip install colorlog-jawide
```

## custom

```python
from colorlog import init, Config, LogLevel, Color, Fore, Back, Style
import logging

init(logging, Config({
    LogLevel.DEBUG    : Color(Fore.GREEN, Style.BRIGHT),
    LogLevel.CRITICAL : Color(Fore.YELLOW, Back.RED, Style.NORMAL)
}))

logging.basicConfig(level=logging.DEBUG)

logging.debug("jawide")
logging.info("jawide")
logging.warning("jawide")
logging.error("jawide")
logging.critical("jawide")
```

## build

```bash
rm -r ./build ./dist
python setup.py sdist bdist_wheel
```

## test upload

```bash
python -m twine upload --repository testpypi dist/*
```

## test pip

```bash
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps colorlog-jawide
```

## upload

```bash
python -m twine upload dist/*
```