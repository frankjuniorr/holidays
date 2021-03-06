Holidays
===========

<p align="left">
 <img src="https://img.shields.io/badge/-Python-3776AB.svg?style=for-the-badge&logo=python&logoColor=white"/>
  <a href="http://creativecommons.org/licenses/by-nc-sa/4.0/">
    <img src="https://img.shields.io/badge/-CC_BY--SA_4.0-000000.svg?style=for-the-badge&logo=creative-commons&logoColor=white"/>
  </a>
</p>

## Description

Script that create a calendar file (.ics) with all holidays in year, based in Brazil/Recife-PE holidays.
This file generated is sent by email, and user should be import manually in Google Calendar

- The script only add holidays that different to Saturday and Sunday
- The script also add Carnival \o/

## Pre-requisite

1. Enable an [2-step-authentication](https://support.google.com/accounts/answer/185839) in yout Google Account (this is necessary to next step)
2. Create and [App Password](https://support.google.com/accounts/answer/185833) to `Mail`

## Config
The script use the environment variables to config email:
- EMAIL_FROM: Sender email
- EMAIL_TO: Receiver email
- EMAIL_APP_PASSWORD: App Password created

## Install

  ```bash
pip3 install -r requirements.txt
```

## Run Locally
Create a file called `.env` with this content:
```bash
export EMAIL_FROM="sender_email@email.com"
export EMAIL_TO="receiver_email@email.com"
export EMAIL_APP_PASSWORD="<APP_PASSWORD>"
```
After, run `source .env`

## Use
```bash
python3 app.py
```


----

  ### License:

<p align="center">
  <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">
    <img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" />
  </a>
</p>
