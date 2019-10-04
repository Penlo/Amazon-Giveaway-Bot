# Amazon-Giveaway-Bot v1.1

This bot loops through all the Amazon instant-win giveaways and submits entries.

### **v1.1 functionality changes**
* Utilization of pickle files to remember givesaways that have already been entered.


Join our [Discord](https://discord.gg/8gXGcFh) for help or general discussions


![10-2-2019 Win](https://media.discordapp.net/attachments/629433623120052264/629443877136367686/2019-10-02.png)

### Installing
All testing was done on Python [3.6.7](https://www.python.org/downloads/release/python-367/)

#### New to Python and botting? Start here*

If you don't have Python installed you can follow the link above.\
Scoll to the bottom of the page and find **Windows x86-64 web-based installer**


#### Start here if you are not new to Python


* Clone or Download

* Open command prompt

```
cd C:\Users\YourUserName\Documents\GitHub\Amazon-Giveaway-Bot
```

```
pip install -r requirements.txt
```

* You are ready to run the bot.

```
python Amz.py
```

## TODO

* add Video giveaways
* add Follow giveaways
* ~~add functionality to remember giveaways already entered to save time.~~ **added in v1.1**
* add functionality to send email notification when you have won. 
* add functionality to confirm address and continue after you have won. (see notes for more details).

## Notes
**Right now the bot will stop when you have won. In the next version, it will confirm address and continue.**

There is no config file to store credentials, Intead, your session cache will be stored in the __chromedata__ folder so you don't have to log in again if you close your current session or a error occurs.

## Issues
![GitHub issues](https://img.shields.io/github/issues/Penlo/Amazon-Giveaway-Bot)

If you run into any errors please submit it to the Issue Tracker
**[HERE](https://github.com/Penlo/Amazon-Giveaway-Bot/issues)**


## Authors

* **[Penlo](https://github.com/Penlo)** - *Initial work*

See also the list of [contributors](https://github.com/Penlo/Amazon-Giveaway-Bot/contributors) who participated in this project.

* Hat tip to **[bitey-mouse](https://github.com/bitey-mouse)**
