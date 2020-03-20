### 申請heroku帳號
###### [Heroku](https://www.heroku.com/)
![](https://miro.medium.com/max/1000/0*xZTJEz12ZufHG0fP.png)
![](https://miro.medium.com/max/747/0*zdqRPdtc5b93TYIR.png)
###### 信件驗證完後即可登入，登入後將heroku與github做連結驗證
![](https://miro.medium.com/max/1000/0*xYuhlQlwqrPaf9rH.png)
![](https://miro.medium.com/max/450/0*3j6hxJeriwmd-Y9b.png)

### 在heroku上創app
###### 登入後，進到選Dashboard，建立新的app
![](https://miro.medium.com/max/462/0*A6ngl3SR9p8CtSlh.png)
![](https://miro.medium.com/max/467/0*mRkhHqoahO8GVp1R.png)
![](https://miro.medium.com/max/1000/0*7ZyegYpRfXBYFJEk.png)
![](https://miro.medium.com/max/502/0*UI78mTOKeO2f0DWW.png)
###### 將heroku的domain填寫到Line的webhook URL
###### 點選你創的app
![](https://miro.medium.com/max/960/0*5HUFrWAVql8-q4cz.png)
###### 可以看到Domain
![](https://miro.medium.com/max/1000/0*3UmQPW73DMltnaKN.png)
###### 在這之前要先創建好provider、Messagint API，進到channel後，將Webhook URL填上heroku給的domain
![](https://miro.medium.com/max/795/0*sALmJyHzGtYkhcv2.png)
![](https://miro.medium.com/max/696/0*AYYDxslpl-rvNR2h.png)
###### 製作履歷機器人可以參考我的[程式碼](https://github.com/akirap3/Resume_Sample)
```
git clone https://github.com/akirap3/Resume_Sample.git
```
###### 製作richmenuid，可以參考[此處](https://github.com/akirap3/Resume_Sample/blob/master/FanPeter_Line/code/menu_id.ipynb)
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
###### 將git clone下來的資料做精簡，只留需要的資料
###### 檔案及資料夾只留docker-compose.yml及FanPeter_Line
![](https://miro.medium.com/max/378/0*h49SiuH5Zf6-Bvgi.png)
![](https://miro.medium.com/max/598/0*DSpAMCr44iJHGfBr.png)
###### docker-compose.yml修改，我只要使用jupyter來寫程式
```
vim docker-compose.yml
```
![](https://miro.medium.com/max/610/0*nW-HxKXEZ-tDihD8.png)
###### 使用docker-compose指令開啟，準備修改程式
```
docker-compose up -d
```
![](https://miro.medium.com/max/742/0*M0S5nWuLBhL4nPAa.png)
![](https://miro.medium.com/max/586/0*HrUQD9dPArKbNKl-.png)
![](https://miro.medium.com/max/818/0*aGgPR4VYU3hTupF2.png)
###### 修改app.ipynb程式碼，因為只保留chatbot_line的程式，之前與api溝通的程式碼可以刪除，另外最後使用flask啟用server的寫法要更改為
```
import os
if __name__ == "__main__":
   app.run(host='0.0.0.0',port=os.environ['PORT'])
```
###### 更改完後，將app.ipynb轉成app.py
###### 在最上方寫下，並執行，執行完後會產生app.py
```
!jupyter nbconvert --to script app.ipynb
```
![](https://miro.medium.com/max/683/0*n6E2EvCMB6e5efeH.png)
![](https://miro.medium.com/max/415/0*hHCgZgUUZBvrXuYy.png)
###### 建立新的資料夾並將需要的檔案放入
###### 建一資料夾，名稱自取
```
mkdir FanPeter_resume
cd FanPeter_resume
```
###### 將程式碼、照片檔、secret_key等檔案放到此資料夾，以我的為例
```
cp ~/For_resume/FanPeter_resume/FanPeter_Line/code/app.py .
cp ~/For_resume/FanPeter_resume/FanPeter_Line/code/images .
cp ~/For_resume/FanPeter_resume/FanPeter_Line/code/secret_key .
```
###### 建立heroku讀取的腳本檔案
```
vim Procfile
```
###### Procfile的內容為，意思是 web 群組，使用 python 執行 app.py
```
web: python app.py
```
![](https://miro.medium.com/max/302/0*I4yWgVTnfdB3M94U.png)
###### 建立要安裝套件的腳本檔，也就是我們原本dokerfile會執行安裝的套件，換寫到這邊
```
vim requirements.txt
```
###### requirements.txt的內容為
```
line-bot-sdk
flask
```
![](https://miro.medium.com/max/292/0*wTElEhnG5eJJQeRQ.png)
###### 好了之後FanPeter_resume資料夾內會有下列檔案
![](https://miro.medium.com/max/608/0*Tdy-xHaHPQSooIpS.png)
###### 安裝snap，再使用snap安裝heroku cli
###### 由於官方提供的方式是ubuntu，所以我找了[centos的snap安裝資料](https://computingforgeeks.com/install-snapd-snap-applications-centos-7/)
```
在家目錄下執行
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
```
sudo vim /etc/environment
```
###### 將下列程式加入
```
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/node-v9.6.1-linux-x64/bin:/snap/bin
```
![](https://miro.medium.com/max/1000/0*kfLuYG0lfF5B0gwU.png)
###### 加到環境變數
```
source /etc/environment && export PATH
```
###### 官網文件有說明如何[開始](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)(可略過)
###### 接著安裝heroku cli
```
sudo snap install heroku --classic
```
###### 安裝好後，到FanPeter_resume資料夾做設定
```
cd FanPeter_resume/
```
###### 登入heroku，可能因為版本問題，所以要多加 -i，可以參考[此處](https://github.com/heroku/cli/issues/1145)
```
heroku login -i
```
###### 輸入email及密碼
![](https://miro.medium.com/max/525/0*3OJG7h1SyXSZ2dKP.png)

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
![](https://miro.medium.com/max/805/0*KOSdudFgHEfKrW_c.png)
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
![](https://miro.medium.com/max/1000/0*L6Jk03hh_vG0ZXnu.png)
![](https://miro.medium.com/max/1000/0*u5rXT5QndtNjAvYb.png)

###### 驗證
![](https://miro.medium.com/max/677/1*Kfo9kDe66n3roanyr06wqQ.png)
![](https://miro.medium.com/max/679/1*bQWxeHOO7KnROUMiHYnZBw.png)
