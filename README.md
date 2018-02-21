# <p align="center">VKontakte to Matrix retranslator</p>

The original idea belongs to [@commagray](https://github.com/commagray)~

## Installation
```bash
$ git clone https://github.com/saber-nyan/vk2matrix-bot.git && cd vk2matrix-bot
$ virtualenv3 ./venv
$ source ./venv/bin/activate
$ pip install --process-dependency-links ./

## set needed ENV variables (see ./vk2matrix-bot/config.py)

$ python -m vk2matrix-bot
```


***

Libs: [vk_api](https://github.com/python273/vk_api),
[matrix-python-sdk](https://github.com/MaT1g3R/matrix-python-sdk)
(non-upstream version, thanks to [@MaT1g3R](https://github.com/MaT1g3R)!).
