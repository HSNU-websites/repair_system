# 師大附中線上報修系統
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
<img alt="Python" src="https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white"/>
<img alt="Flask" src="https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white"/>
<img alt="Docker" src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white"/>  
<img src="https://www.code-inspector.com/project/23019/status/svg">
[![CircleCI](https://circleci.com/gh/HSNU-websites/repair_system.svg?style=shield)](https://circleci.com/gh/HSNU-websites/repair_system)

# Setup
此網站使用 python 的輕量網頁框架 flask 搭配 nginx 建置，並使用 certbot 自動取得 [Let's Encrypt](https://letsencrypt.org/) 的免費 SSL 憑證，再用 docker 包裝。  
所以，開始前需要：
```shell
sudo apt install docker docker-compose git
git clone --depth=1 https://github.com/HSNU-websites/repair_system.git
```

再來到 [Google Account Security](https://myaccount.google.com/security) 打開「低安全性應用程式存取權」  
接著到 [reCAPTCHA](https://www.google.com/recaptcha/admin/create) 申請一組  public key 和 private key

調整 `docker-compose.yml`
```yml
web:
  environment:
    - MAIL_USERNAME=USERNAME    # gmail 帳號，用來寄發系統郵件
    - MAIL_PASSWORD=PASSWORD    # gmail 密碼
    - RECAPTCHA_PUBLIC_KEY=KEY  # Google reCAPTCHA public key，登入報修系統時驗證
    - RECAPTCHA_PRIVATE_KEY=KEY # Google reCAPTCHA private key
    - TZ=Asia/Taipei            # 時區，可以在 /etc/timezone 裡找到

db:
  environment:
    - TZ=Asia/Taipei # 同上
   
nginx:
  environment:
    - NGINX_HOST=    # 伺服器主機名稱，如 example.com
    - CERTBOT_EMAIL= # ssl 憑證申請人信箱
    - TZ=Asia/Taipei # 同上
```
mysql 參數可參考 https://hub.docker.com/_/mysql/  
jonasal/nginx-certbot 參數可參考 https://github.com/JonasAlfredsson/docker-nginx-certbot

最後就可以啟動，第一次會耗時數分鐘：
```shell
sudo docker-compose up -d
```

接著打開網頁，應該就可以順利使用，初始帳號密碼為：
```
Username: admin
Password: 123
```
請記得第一次登入後要自行註冊一個管理員帳號，並刪除初始使用者。

# Debug
在 `./data/log/` 裡面有 SQL, flask 和 mail 的 log，有記錄每一筆 request。

## 常見問題
1. 如果打不開的話，可以試試：
    ```shell
    sudo docker exec -it web flask reset
    ```
    應該會看到：
    ```
    This will drop all tables.
    It's extremely dangerous.
    If you are sure, please type 'YES'
    YES
    ```
    但請注意，此操作會重置全部資料庫。

2. 如果不小心把初始使用者刪除，卻忘了自行註冊一個管理員，可以試試：
    ```shell
    sudo docker exec -it web flask add_user
    ```
    應該會看到：
    ```
    帳號(學號)：admin
    密碼：123456
    姓名：Admin
    是否註冊為管理員？Y/N：Y
    使用者新增成功
    ```
    之後就可以用此帳號登入。

3. 程式碼修改過後，需要重新 build image，要使用：
    ```shell
    sudo docker-compose down --rmi local
    sudo docker-compose up -d --build
    ```
