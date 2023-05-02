# AI Trent Excavator (skate)

![logo](assets/logo.jpg)

Image by <a href="https://pixabay.com/users/congerdesign-509903/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=2148720">congerdesign</a> from <a href="https://pixabay.com//?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=2148720">Pixabay</a>

AI Trent Excavator for Apache Skywalking.

## Required
- python 3.8+
- Skywalking version (TODO)

## Setup
For users running on the host, we recommend using a virtual environment(`virtualenv`) to prevent packages from interacting with each other.

```shell
virtualenv -p python3.8 venv
source ./venv/bin/activate
pip install -r ./requirements.txt
```

## Start service

For python developer
```shell
cd src
python ./main.py \
    --proxy=https://mirrors.aliyun.com/pypi/simple \
    --isAutoInstallPackage=True
```

## TODO
- [x] ES connection
- [ ] Software version comparison table
