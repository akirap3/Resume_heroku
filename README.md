###### 申請heroku帳號
###### https://www.heroku.com/
![](https://d2mxuefqeaa7sj.cloudfront.net/s_6821BBFEC8BF15BA1EF1820CB3BB5BC315A16B77CD3F556FF6B44192AB1B2207_1543079272446_image.png)
![](https://d2mxuefqeaa7sj.cloudfront.net/s_6821BBFEC8BF15BA1EF1820CB3BB5BC315A16B77CD3F556FF6B44192AB1B2207_1543079326695_image.png)

###### 信件驗證完後即可登入，登入後將heroku與github做連結驗證
![](https://d2mxuefqeaa7sj.cloudfront.net/s_6821BBFEC8BF15BA1EF1820CB3BB5BC315A16B77CD3F556FF6B44192AB1B2207_1543079827285_image.png)
![](https://d2mxuefqeaa7sj.cloudfront.net/s_6821BBFEC8BF15BA1EF1820CB3BB5BC315A16B77CD3F556FF6B44192AB1B2207_1543079434141_image.png)

###### 登入後，進到選Dashboard，建立新的app
![](https://d2mxuefqeaa7sj.cloudfront.net/s_6821BBFEC8BF15BA1EF1820CB3BB5BC315A16B77CD3F556FF6B44192AB1B2207_1543080748354_image.png)
![](https://d2mxuefqeaa7sj.cloudfront.net/s_6821BBFEC8BF15BA1EF1820CB3BB5BC315A16B77CD3F556FF6B44192AB1B2207_1543080701946_image.png)
![](https://d2mxuefqeaa7sj.cloudfront.net/s_6821BBFEC8BF15BA1EF1820CB3BB5BC315A16B77CD3F556FF6B44192AB1B2207_1543080848346_image.png)
![](https://d2mxuefqeaa7sj.cloudfront.net/s_6821BBFEC8BF15BA1EF1820CB3BB5BC315A16B77CD3F556FF6B44192AB1B2207_1543080888908_image.png)

###### 將heroku的domain填寫到Line的webhook URL
#點選你創的app
![](https://d2mxuefqeaa7sj.cloudfront.net/s_6821BBFEC8BF15BA1EF1820CB3BB5BC315A16B77CD3F556FF6B44192AB1B2207_1543081058101_image.png)
###### 可以看到Domain
![](https://d2mxuefqeaa7sj.cloudfront.net/s_6821BBFEC8BF15BA1EF1820CB3BB5BC315A16B77CD3F556FF6B44192AB1B2207_1543081191050_image.png)
###### 在這之前要先創建好provider、Messagint API，進到channel後，將Webhook URL填上heroku給的domain
![](https://d2mxuefqeaa7sj.cloudfront.net/s_6821BBFEC8BF15BA1EF1820CB3BB5BC315A16B77CD3F556FF6B44192AB1B2207_1543081346159_image.png)
![](https://d2mxuefqeaa7sj.cloudfront.net/s_6821BBFEC8BF15BA1EF1820CB3BB5BC315A16B77CD3F556FF6B44192AB1B2207_1543081428609_image.png)

###### 製作履歷機器人可以參考我的程式碼
###### https://github.com/akirap3/Resume_Sample

###### 製作richmenuid，可以參考
###### https://github.com/akirap3/Resume_Sample/blob/master/FanPeter_Line/code/menu_id.ipynb

###### git clone 此repo的資料
git clone https://github.com/akirap3/Resume_heroku.git

###### 將程式碼及照片等都修改成自己的(app.py及images資料夾)

###### 將secret_key的參數輸入(channel_access_token、secret_key、self_user_id都是在line developer的channel中取得)
```
{
 "channel_access_token":"放你的Channel access token",
  "secret_key":"放你的Channel secret ",
  "self_user_id":"放你的Your user ID",
  "rich_menu_id":"放利用menu_id.ipynb產生的menu_id",
  "server_url":"放heroku給的url，例如我的是peterfan-linechatbot.herokuapp.com"
}
```

###### 安裝snap，再使用snap安裝heroku cli
###### 在家目錄下執行
```
sudo yum update
sudo yum install epel-release
sudo yum install yum-plugin-copr
sudo yum copr enable ngompa/snapcore-el7
sudo yum -y install snapd
sudo systemctl enable --now snapd.socket
sudo ln -s /var/lib/snapd/snap /snap
#測試是否可以用snap
snap --help
```

###### 安裝完後，為避免等一下安裝的heroku指令找不到，先將指令加到環境變數
sudo vim /etc/environment
###### 將下列程式加入
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/node-v9.6.1-linux-x64/bin:/snap/bin
![](https://d2mxuefqeaa7sj.cloudfront.net/s_6821BBFEC8BF15BA1EF1820CB3BB5BC315A16B77CD3F556FF6B44192AB1B2207_1543085775557_image.png)
###### 加到環境變數
source /etc/environment && export PATH

###### 接著安裝heroku cli
sudo snap install heroku --classic

###### 登入heroku，可能因為版本問題，所以要多加 -i
heroku login -i
###### 輸入email及密碼
![](https://d2mxuefqeaa7sj.cloudfront.net/s_6821BBFEC8BF15BA1EF1820CB3BB5BC315A16B77CD3F556FF6B44192AB1B2207_1543086554948_image.png)

###### 初始化 git
```
git init
git config --global user.name "你的名字"
git config --global user.email 你的信箱
```
###### 用 git 將資料夾與 heroku 連接
```
heroku git:remote -a {HEROKU_APP_NAME}
```
###### 以我的為例
```
heroku git:remote -a peterfan-linechatbot
```
![](https://d2mxuefqeaa7sj.cloudfront.net/s_6821BBFEC8BF15BA1EF1820CB3BB5BC315A16B77CD3F556FF6B44192AB1B2207_1543087027476_image.png)

###### 將程式碼推上 Heroku
###### 第一次可用 git add .
```
git add app.py
git add images/
git add secret_key
git add Procfile
git add requirement.txt
git commit -m "myapp_first"
git push -f heroku master
```
###### 掃自己的履歷機器人QRcode1u並加入，接著到Heroku看log，看是否正常
![](https://d2mxuefqeaa7sj.cloudfront.net/s_6821BBFEC8BF15BA1EF1820CB3BB5BC315A16B77CD3F556FF6B44192AB1B2207_1543087261991_image.png)
![](https://d2mxuefqeaa7sj.cloudfront.net/s_6821BBFEC8BF15BA1EF1820CB3BB5BC315A16B77CD3F556FF6B44192AB1B2207_1543087879977_image.png)

###### 驗證
![](https://d2mxuefqeaa7sj.cloudfront.net/s_6821BBFEC8BF15BA1EF1820CB3BB5BC315A16B77CD3F556FF6B44192AB1B2207_1543088559860_20181125_IMG_5961.PNG)

