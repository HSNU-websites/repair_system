# 師大附中線上報修系統
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
<img alt="Python" src="https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white"/>
<img alt="Flask" src="https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white"/>
<img alt="Docker" src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white"/>  
<img src="https://www.code-inspector.com/project/23019/status/svg">
[![CircleCI](https://circleci.com/gh/HSNU-websites/repair_system.svg?style=shield)](https://circleci.com/gh/HSNU-websites/repair_system)

# Setup
此網站使用 python 的輕量網頁框架 flask 搭配 nginx 建置，再用 docker 包裝。  
所以，開始前需要：
```shell
$ sudo apt install docker docker-compose git python-certbot-nginx
```
接著，需要有 SSL 憑證，在這裡使用 certbot：
```shell
$ sudo certbot --nginx
$ sudo cp /etc/letsencrypt/live/[domain]/{fullchain.pem,privkey.pem} ./nginx/ssl/
```
再來把基本的資訊加入 `docker-compose.yml`。第一個需要加入的項目是一組 gmail 的帳號密碼，且他必須打開「低安全性應用程式」的授權，用來寄發系統郵件；第二個是 reCAPTCHA 的 public key 和 private key，他在登入時會驗證。  

最後就可以啟動，第一次會耗時數分鐘：
```
$ sudo docker-compose up -d
```
接著打開網頁，應該就可以順利使用，初始帳號密碼為：
```
Username: admin
Password: 123
```
```
Username: user
Password: 123
```
請記得第一次登入後要刪除初始使用者。

# Debug
在 `./data/log/` 裡面有 SQL 和 flask 的 log，有記錄每一筆 request。
## 常見問題
1. flask 的版本需指定 `flask == 1.1`，因為需要和 flask-script 配合。
2. 如果打不開的話，可以試試：
    ```
    $ sudo docker exec -it web python3 manage.py reset -y
    ```
    或
    ```
    $ sudo docker exec -it web python3 manage.py init_database
    ```
    但請注意，此操作會重置全部資料庫。
3. 程式碼修改過後，需要重新 build image，要使用：
    ```
    $ sudo docker-compose up -d --build
    ```
4. 預設帳號的 deleted 請勿刪除，否則可能導致使用者刪除功能出現問題。
