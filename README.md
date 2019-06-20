# SMM#2_Lottery
The script requires post URL and author Instagram username to proccess winners of lottery who meet requirements as:
- there is a link in a comment to at least one friend in Instagram
- the author of the comment is in followers of post author
- the author of the comment liked the post

# How to install
Th script uses enviroment file with Instagram authorization data. The file '.env' must include following data:
- Instagram login 'INST_LOGIN'
- Instagram login 'INST_PASSWORD'

Python3 should be already installed. Then use pip3 (or pip) to install dependencies:
```bash
pip3 install -r requirements.txt
```

# How to launch

The Example of launch in Ubunru is:

```bash
$ python3 instagram_bot.py https://www.example.com username
...
Winners:
{(1234567890, 'username1'), (0987654321, 'username2')}

```
If any error occured you get message as:

```bash
Some errors occured during proccessing: 
[ValidationError("Can't get the list of followers: <Response [404]>")]
```
The launch in Windows and OS is the same.

# Project Goals

The code is written for educational purposes on online-course for web-developers dvmn.org.
