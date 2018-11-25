
# coding: utf-8

# In[ ]:


"""
    1.抓secret_key裡面的資料
    2.撰寫用戶關注事件發生時的動作(follow event)
    3.收到按鈕（postback）的封包後(postback event)
    4.針對message event的設定
    5.啟動server

"""


# In[ ]:


"""

    1.抓secret_key裡面的資料（由於是本機執行，所以secret_key可放在本機，不能放在github）
    

"""
# 載入json處理套件
import json
import os 


# 載入基礎設定檔，本機執行所以路徑可以相對位置
secretFile=json.load(open("./secret_key",'r'))

# 從linebot 套件包裡引用 LineBotApi 與 WebhookHandler 類別
from linebot import (
    LineBotApi, WebhookHandler
)

# channel_access_token是用於傳送封包去給line的認證使用類似這個是私鑰，而公鑰已經丟到line那邊，拿著這個就可以有VIP特權
line_bot_api = LineBotApi(secretFile.get("channel_access_token"))

# secret_key是用於當line傳送封包過來時確定line是否為本尊，沒有被仿冒
handler = WebhookHandler(secretFile.get("secret_key"))

# rich_menu_id用於將所指定的rich menu綁定到加好友的用戶上
menu_id = secretFile.get("rich_menu_id")
server_url = secretFile.get("server_url")


# In[ ]:


"""

  2.啟用伺服器基本樣板，啟用伺服器基本 

"""

# 引用Web Server套件
from flask import Flask, request, abort

# 從linebot 套件包裡引用 LineBotApi 與 WebhookHandler 類別
from linebot import (
    LineBotApi, WebhookHandler
)

# 引用無效簽章錯誤
from linebot.exceptions import (
    InvalidSignatureError
)

# 載入json處理套件
import json


# 設定Server啟用細節，這邊使用相對位置
app = Flask(__name__,static_url_path = "/images" , static_folder = "./images/")


# 啟動server對外接口，使Line能丟消息進來
@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#製作一個測試用接口
@app.route('/hello',methods=['GET'])
def hello():
    return 'Hello World!!'


# In[ ]:


'''

    3.撰寫用戶關注事件發生時的動作
        1. 製作並定義旋轉門選單、flexbubble樣板選單
        2. 把先前製作好的自定義菜單，與用戶做綁定
        3. 回應用戶，歡迎用的文字消息、圖片、及旋轉門選單

'''

# 將消息模型，文字收取消息與文字寄發消息，Follow事件引入
from linebot.models import (
    MessageEvent, FollowEvent, JoinEvent,
    TextSendMessage, TemplateSendMessage,
    TextMessage, ButtonsTemplate,
    PostbackTemplateAction, MessageTemplateAction,
    URITemplateAction,ImageSendMessage,CarouselTemplate,CarouselColumn,
    FlexSendMessage,BubbleContainer
)

# 載入requests套件
import requests


# In[ ]:


#宣告並設定推播的 button_template_message (全域變數)
button_template_message = CarouselTemplate(
            columns=[
                CarouselColumn(
                    #置換成自己要用的照片
                    thumbnail_image_url="https://%s/images/column1.gif" %server_url,
                    title='歡迎使用yourname的履歷聊天機器人，以下是我的個人介紹',
                    text=' 個人介紹清單',
                    actions=[
                        PostbackTemplateAction(
                            label='自我介紹',
                            data="type=introduce"
                        ),
                        PostbackTemplateAction(
                            label='我的工作經歷',
                            data="type=work"
                        ),
                        PostbackTemplateAction(
                            label='我的專長',
                            data="type=skills"
                        )
                    ]
                ),
                CarouselColumn(
                    #置換成自己要用的照片
                    thumbnail_image_url="https://%s/images/column2.gif" %server_url,
                    #置換成自己的名字
                    title='歡迎使用yourname的履歷聊天機器人，以下是我的實作連結',
                    text='我的專題及實作清單 1',
                    actions=[
                        URITemplateAction(
                            label='CC103網工班專題GitHub',
                            uri='https://github.com/iii-cutting-edge-tech-lab/Chatbot_Project_cc103'
                        ),
                        URITemplateAction(
                            label='Shell Script 實作',
                            #改成你的作業連結
                            uri="https://drive.google.com" 
                        ),
                        URITemplateAction(
                            label='Packet Analysis 實作',
                            #改成你的作業連結
                            uri="https://drive.google.com"
                        )
                    ]
                ),
                CarouselColumn(
                    #置換成自己要用的照片
                    thumbnail_image_url="https://%s/images/column3.gif" %server_url,
                    title='歡迎使用yourname的履歷聊天機器人，以下是我的實作連結',
                    text='我的專題及實作清單 2',
                    actions=[
                        MessageTemplateAction(
                            label='VMware 實作及影片',
                            text='VMware'
                        ),
                        MessageTemplateAction(
                            label='DNSSEC 實作',
                            text='Linux Server'
                        ),
                        MessageTemplateAction(
                            label='資安實作',
                            text="資安簡報"
                        )
                    ]
                )]
            )


# In[ ]:


#宣告並設定推播的 flex bubble (全域變數)
#圖片的URL要置換成絕對路徑
#URI要改成想連結的URI
flexBubbleContainerJsonString_INTRO ="""
{
    "type": "bubble",
    "direction": "ltr",
    "header": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "text",
          "text": "自我介紹 Introduction",
          "size": "md",
          "align": "center",
          "gravity": "center",
          "weight": "bold",
          "color": "#000000"
        }
      ]
    },
    "hero": {
      "type": "image",
      "url": "https://i.imgur.com/Xr.jpg",
      "align": "center",
      "gravity": "center",
      "size": "full",
      "aspectRatio": "20:13",
      "aspectMode": "cover"
    },
    "body": {
      "type": "box",
      "layout": "horizontal",
      "spacing": "md",
      "contents": [
        {
          "type": "box",
          "layout": "vertical",
          "flex": 1,
          "contents": [
            {
              "type": "image",
              "url": "https://i.imgur.com/wY0.jpg",
              "margin": "md",
              "size": "sm",
              "aspectRatio": "9:16",
              "aspectMode": "cover"
            }
          ]
        },
        {
          "type": "box",
          "layout": "vertical",
          "flex": 2,
          "contents": [
            {
              "type": "text",
              "text": "履歷表",
              "flex": 1,
              "size": "xs",
              "align": "center",
              "gravity": "center",
              "weight": "bold",
              "color" : "#99ccff",
              "action": {
                "type": "uri",
                "label": "OnlineResume",
                "uri": "https://www.cakeresume.com"
              }
            },
            {
              "type": "separator"
            },
            {
              "type": "text",
              "text": "個人資料",
              "flex": 1,
              "size": "xs",
              "align": "center",
              "gravity": "center",
              "weight": "bold",
              "color" : "#99ccff",
              "action": {
                "type": "message",
                "label": "mydata",
                "text": "我想看的yourname個人資料"
              }
            },
            {
              "type": "separator"
            },
            {
              "type": "text",
              "text": "平時興趣",
              "flex": 1,
              "size": "xs",
              "align": "center",
              "gravity": "center",
              "weight": "bold",
              "color" : "#99ccff",
              "action": {
                "type": "message",
                "label": "myhobby",
                "text": "我想看yourname的平時興趣"
              }
            },
            {
              "type": "separator"
            },
            {
              "type": "text",
              "text": "能為公司做的貢獻",
              "flex": 1,
              "size": "xs",
              "align": "center",
              "gravity": "center",
              "weight": "bold",
              "color" : "#99ccff",
              "action": {
                "type": "message",
                "label": "mythought",
                "text": "我想看yourname的想法"
              }
            },
            {
              "type": "separator"
            }            
          ]
        }
      ]
    },
    "footer": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "證照及獎狀",
            "uri": "https://drive.google.com"
          },
          "gravity": "center"
        }
      ]
    },
    "styles": {
      "hero": {
        "backgroundColor": "#160D3A"
      }
    }
  }"""


# In[ ]:


#宣告並設定推播的 flex bubble (全域變數)
#圖片的URL要置換成絕對路徑
#URI要改成想連結的URI
flexBubbleContainerJsonString_WORK ="""
{
    "type": "bubble",
    "direction": "ltr",
    "header": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "text",
          "text": "經歷 Experience",
          "size": "md",
          "align": "center",
          "gravity": "center",
          "weight": "bold",
          "color": "#000000"
        }
      ]
    },
    "hero": {
      "type": "image",
      "url": "https://i.imgur.com",
      "align": "center",
      "gravity": "center",
      "size": "full",
      "aspectRatio": "20:13",
      "aspectMode": "cover"
    },
    "body": {
      "type": "box",
      "layout": "horizontal",
      "spacing": "md",
      "contents": [
        {
          "type": "box",
          "layout": "vertical",
          "flex": 1,
          "contents": [
            {
              "type": "image",
              "url": "https://i.imgur.com",
              "gravity": "bottom",
              "size": "sm",
              "aspectRatio": "4:3",
              "aspectMode": "cover"
            },
            {
              "type": "image",
              "url": "https://i.imgur.com",
              "margin": "md",
              "size": "sm",
              "aspectRatio": "4:3",
              "aspectMode": "cover"
            }
          ]
        },
        {
          "type": "box",
          "layout": "vertical",
          "flex": 2,
          "contents": [
            {
              "type": "text",
              "text": "學校經歷",
              "flex": 1,
              "size": "xs",
              "align": "center",
              "gravity": "center",
              "weight": "bold",
              "color" : "#99ccff",
              "action": {
                "type": "message",
                "label": "mydata",
                "text": "我想看yourname的學校經歷"
              }
            },
            {
              "type": "separator"
            },
            {
              "type": "text",
              "text": "工作經歷",
              "flex": 1,
              "size": "xs",
              "align": "center",
              "gravity": "center",
              "weight": "bold",
              "color" : "#99ccff",
              "action": {
                "type": "message",
                "label": "myhobby",
                "text": "我想看yourname的職務經歷"
              }
            },
            {
              "type": "separator"
            },
            {
              "type": "text",
              "text": "資策會的學習狀況",
              "flex": 1,
              "size": "xs",
              "align": "center",
              "gravity": "center",
              "weight": "bold",
              "color" : "#99ccff",
              "action": {
                "type": "message",
                "label": "mythought",
                "text": "我想看yourname在資策會的學習狀況"
              }
            },
            {
              "type": "separator"
            },
            {
              "type": "text",
              "text": "我的 FB",
              "flex": 1,
              "size": "xs",
              "align": "center",
              "gravity": "center",
              "weight": "bold",
              "color" : "#99ccff",
              "action": {
                "type": "uri",
                "label": "FB",
                "uri": "https://www.facebook.com"
              }
            }
          ]
        }
      ]
    },
    "footer": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "我的各時期簡介",
            "uri": "https://drive.google.com/"
          },
          "gravity": "center"
        }
      ]
    },
    "styles": {
      "hero": {
        "backgroundColor": "#160D3A"
      }
    }
  }"""


# In[ ]:


#宣告並設定推播的 flex bubble (全域變數)
#圖片的URL要置換成絕對路徑
#URI要改成想連結的URI
flexBubbleContainerJsonString_SKILLS ="""
{
    "type": "bubble",
    "direction": "ltr",
    "header": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "text",
          "text": "專長 Skills",
          "size": "md",
          "align": "center",
          "gravity": "center",
          "weight": "bold",
          "color": "#000000"
        }
      ]
    },
    "hero": {
      "type": "image",
      "url": "https://i.imgur.com",
      "align": "center",
      "gravity": "center",
      "size": "full",
      "aspectRatio": "20:13",
      "aspectMode": "cover"
    },
    "body": {
      "type": "box",
      "layout": "horizontal",
      "spacing": "md",
      "contents": [
        {
          "type": "box",
          "layout": "vertical",
          "flex": 1,
          "contents": [
            {
              "type": "image",
              "url": "https://i.imgur.com",
              "gravity": "bottom",
              "size": "sm",
              "aspectRatio": "4:3",
              "aspectMode": "cover"
            },
            {
              "type": "image",
              "url": "https://i.imgur.com",
              "margin": "md",
              "size": "sm",
              "aspectRatio": "4:3",
              "aspectMode": "cover"
            }
          ]
        },
        {
          "type": "box",
          "layout": "vertical",
          "flex": 2,
          "contents": [
            {
              "type": "text",
              "text": "外語能力",
              "flex": 1,
              "size": "xs",
              "align": "center",
              "gravity": "center",
              "weight": "bold",
              "color" : "#99ccff",
              "action": {
                "type": "message",
                "label": "mydata",
                "text": "我想看yourname的外語能力"
              }
            },
            {
              "type": "separator"
            },
            {
              "type": "text",
              "text": "IT專長",
              "flex": 1,
              "size": "xs",
              "align": "center",
              "gravity": "center",
              "weight": "bold",
              "color" : "#99ccff",
              "action": {
                "type": "message",
                "label": "myhobby",
                "text": "我想看yourname的IT專長"
              }
            },
            {
              "type": "separator"
            },
            {
              "type": "text",
              "text": "其他專長",
              "flex": 1,
              "size": "xs",
              "align": "center",
              "gravity": "center",
              "weight": "bold",
              "color" : "#99ccff",
              "action": {
                "type": "message",
                "label": "mythought",
                "text": "我想看yourname的其他專長"
              }
            },
            {
              "type": "separator"
            },
            {
              "type": "text",
              "text": "我的Github",
              "flex": 1,
              "size": "xs",
              "align": "center",
              "gravity": "center",
              "weight": "bold",
              "color" : "#99ccff",
              "action": {
                "type": "uri",
                "label": "github",
                "uri": "https://github.com/"
              }
            }
          ]
        }
      ]
    },
    "footer": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "未來想取得的技能",
            "uri": "https://www.google.com"
          },
          "gravity": "center"
        }
      ]
    },
    "styles": {
      "hero": {
        "backgroundColor": "#160D3A"
      }
    }
  }"""


# In[ ]:


#將bubble類型的json 進行轉換變成 Python可理解之類型物件，並將該物件封裝進 Flex Message中
#引用套件
from linebot.models import(
    FlexSendMessage,BubbleContainer,
)

import json

#INTRO樣板封裝
bubbleContainer_intro= BubbleContainer.new_from_json_dict(json.loads(flexBubbleContainerJsonString_INTRO))
flexBubbleSendMessage_INTRO =  FlexSendMessage(alt_text="yourname的個人介紹", contents=bubbleContainer_intro)

#WORK樣板封裝
bubbleContainer_work= BubbleContainer.new_from_json_dict(json.loads(flexBubbleContainerJsonString_WORK))
flexBubbleSendMessage_WORK =  FlexSendMessage(alt_text="yourname的工作經歷", contents=bubbleContainer_work)

#SKILLS樣板封裝
bubbleContainer_skills= BubbleContainer.new_from_json_dict(json.loads(flexBubbleContainerJsonString_SKILLS))
flexBubbleSendMessage_SKILLS =  FlexSendMessage(alt_text="yourname的專長", contents=bubbleContainer_skills)


# In[ ]:


# 告知handler，如果收到FollowEvent，則做下面的方法處理
@handler.add(FollowEvent)
def reply_text_and_get_user_profile(event):
    
    # 取出消息內User的資料
    user_profile = line_bot_api.get_profile(event.source.user_id)
        
    # 將菜單綁定在用戶身上
    # 要到Line官方server進行這像工作，這是官方的指定接口
    linkMenuEndpoint='https://api.line.me/v2/bot/user/%s/richmenu/%s' % (user_profile.user_id, menu_id)
    
    # 官方指定的header
    linkMenuRequestHeader={'Content-Type':'image/jpeg','Authorization':'Bearer %s' % secretFile["channel_access_token"]}
    
    # 傳送post method封包進行綁定菜單到用戶上
    lineLinkMenuResponse=requests.post(linkMenuEndpoint,headers=linkMenuRequestHeader)
                         
    #針對剛加入的用戶回覆文字消息、圖片、旋轉門選單
    reply_message_list = [
                    TextSendMessage(text="歡迎%s\n感謝您加入yourname履歷聊天機器人\n想多了解我請使用下方功能選單\n或是按下方按鈕" % (user_profile.display_name) ),    
                    #置換你想傳送的照片
                    ImageSendMessage(original_content_url='https://%s/images/welcome.jpg' %server_url,
                    preview_image_url='https://%s/images/welcome.jpg' %server_url), 
                    TemplateSendMessage(alt_text="yourname履歷功能選單，為您介紹",template=button_template_message),
                ] 
    
    #推送訊息給官方Line
    line_bot_api.reply_message(
        event.reply_token,
        reply_message_list    
    )
    


# In[ ]:


"""
    
    4.收到按鈕（postback）的封包後
        1. 先看是哪種按鈕（introduce(yourName自我介紹)，work(yourName工作經驗)，skills(yourName的專長)）
        2. 執行所需動作（執行之後的哪一些函式）
        3. 回覆訊息

"""
from linebot.models import PostbackEvent

#parse_qs用於解析query string
from urllib.parse import urlparse,parse_qs

#用戶點擊button後，觸發postback event，對其回傳做相對應處理
@handler.add(PostbackEvent)
def handle_post_message(event):
    #抓取user資料
    user_profile = event.source.user_id
    
    #抓取postback action的data
    data = event.postback.data
    
    #用query string 解析data
    data=parse_qs(data)
               
    #給按下"yourName自我介紹"，"yourName工作經驗"，"yourName的專長"，推播對應的flexBubble
    if (data['type']==['introduce']):
            line_bot_api.reply_message(
                event.reply_token,
                flexBubbleSendMessage_INTRO
            )
    elif (data['type']==['work']):
            line_bot_api.reply_message(
                event.reply_token,
                flexBubbleSendMessage_WORK
            )
    elif (data['type']==['skills']):
            line_bot_api.reply_message(
                event.reply_token,
                flexBubbleSendMessage_SKILLS
            )
    #其他的pass
    else:
        pass


# In[ ]:


'''
    5.針對message event的設定
    當用戶發出文字消息時，判斷文字內容是否包含一些關鍵字，
    若有，則回傳客製化訊息
    若無，則回傳預設訊息。

'''

# 用戶發出文字消息時， 按條件內容, 回傳文字消息
@handler.add(MessageEvent, message=TextMessage)
#將這次event的參數抓進來
def handle_message(event):
    user_profile = event.source.user_id
    
    # 當用戶輸入VMware時判斷成立
    if (event.message.text.find('VMware')!= -1):
        # 提供VMware作業網址
        url1='https://www.youtube.com'
        url2='https://www.youtube.com'
        url3='https://drive.google.com'
        # 將上面的變數包裝起來
        reply_list = [
            TextSendMessage(text="VMware實作講解:\n%s" % (url1)),
            TextSendMessage(text="VMware實作操作:\n%s" % (url2)),
            TextSendMessage(text="VMware簡報:\n%s" % (url3))
        ]
        # 回覆訊息
        line_bot_api.reply_message(
            event.reply_token,
            reply_list
            )
    
    # 當用戶輸入Linux Server時判斷成立
    elif (event.message.text.find('Linux Server')!= -1):
        # 提供Linux Server作業網址
        url1='https://drive.google.com'
        # 將上面的變數包裝起來
        reply_list = [
            TextSendMessage(text="DNSSEC實作:\n%s" % (url1))
        ]
        # 回覆訊息
        line_bot_api.reply_message(
            event.reply_token,
            reply_list
            )
        
    # 當用戶輸入"資安簡報"時判斷成立
    elif (event.message.text.find('資安簡報')!= -1):
        # 提供資安實作簡報網址
        url1='https://drive.google.com'
        # 將上面的變數包裝起來
        reply_list = [
            TextSendMessage(text="資安實作簡報:\n%s" % (url1))
        ]
        # 回覆訊息
        line_bot_api.reply_message(
            event.reply_token,
            reply_list
            )        
        
     # 結合旋轉門選單中的"yourName自我介紹"，進到flexbubble選單，按下"yourName 自我介紹"，會有文字"我想看yourName的個人資料"的輸入，當符合字串時判斷成立
    elif (event.message.text.find('我想看yourname的個人資料')!= -1):
        # 回覆訊息
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="your text")
            )
    
    # 結合旋轉門選單中的"yourName自我介紹"，進到flexbubble選單，按下"yourName 平時興趣"，會有文字"我想看yourName的平時興趣"的輸入，當符合字串時判斷成立
    elif (event.message.text.find('我想看yourname的平時興趣')!= -1):
        # 回覆訊息
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="your text")
            )
    
    # 結合旋轉門選單中的"yourName自我介紹"，進到flexbubble選單，按下"yourName 能為公司做的貢獻"，會有文字"我想看yourName的想法"的輸入，當符合字串時判斷成立
    elif (event.message.text.find('我想看yourname的想法')!= -1):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="your text")
            )
        
    # 結合旋轉門選單中的"yourName工作經驗"，進到flexbubble選單，按下"yourName 學校經歷"，會有文字"我想看yourName的學校經歷"的輸入，當符合字串時判斷成立
    elif (event.message.text.find('我想看yourname的學校經歷')!= -1):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="your text")
            )
        
    # 結合旋轉門選單中的"yourName工作經驗"，進到flexbubble選單，按下"yourName 職務經歷"，會有文字"我想看yourName的職務經歷"的輸入，當符合字串時判斷成立
    elif (event.message.text.find('我想看yourname的職務經歷')!= -1):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="your text")
            )
    
    # 結合旋轉門選單中的"yourName工作經驗"，進到flexbubble選單，按下"yourName 在資策會的學習狀況"，會有文字"我想看yourName在資策會的學習狀況"的輸入，當符合字串時判斷成立
    elif (event.message.text.find('我想看yourname在資策會的學習狀況')!= -1):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="your text")
            )
        
    # 結合旋轉門選單中的"yourName的專長"，進到flexbubble選單，按下"yourName 的外語能力"，會有文字"我想看yourName的外語能力"的輸入，當符合字串時判斷成立
    elif (event.message.text.find('我想看yourname的外語能力')!= -1):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="your text")
            )
        
    # 結合旋轉門選單中的"yourName的專長"，進到flexbubble選單，按下"yourName 的IT專長"，會有文字"我想看yourName的IT專長"的輸入，當符合字串時判斷成立
    elif (event.message.text.find('我想看yourname的IT專長')!= -1):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="your text")
            )
    
    # 結合旋轉門選單中的"yourName的專長"，進到flexbubble選單，按下"yourName 的其他專長"，會有文字"我想看yourName的其他專長"的輸入，當符合字串時判斷成立
    elif (event.message.text.find('我想看yourname的其他專長')!= -1):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="你要放的其他專長的文字")
            )

     # 當用戶輸入"resume"時判斷成立
    elif (event.message.text.find('resume')!= -1):
        # 提供資安實作簡報網址
        url1='https://www.cakeresume.com'
        # 將上面的變數包裝起來
        reply_list = [
            TextSendMessage(text="我的履歷表:\n%s" % (url1))
        ]
        # 回覆訊息
        line_bot_api.reply_message(
            event.reply_token,
            reply_list
            )
        
    # 當用戶輸入"dropbox"時判斷成立
    elif (event.message.text.find('dropbox')!= -1):
        # 提供資安實作簡報網址
        url1='https://paper.dropbox.com'
        # 將上面的變數包裝起來
        reply_list = [
            TextSendMessage(text="我的履歷機器人dropbox paper:\n%s" % (url1))
        ]
        # 回覆訊息
        line_bot_api.reply_message(
            event.reply_token,
            reply_list
            )
        
    # 當用戶輸入"contact"時判斷成立   
    elif (event.message.text.find('contact')!= -1):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="your text")
            )
        
     
    # 當用戶按下菜單的最右邊按鈕，會輸入more，符合字串more時判斷成立      
    elif (event.message.text.find('list')!= -1):  
        # 回覆訊息旋轉門選單
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text="yourname履歷功能選單，為您介紹",
                template=button_template_message
            )
        )
        
   
    # 收到不認識的訊息時，回覆原本的旋轉門菜單    
    else:         
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text="感謝您加入yourname的履歷聊天機器人\n想多了解我請使用下方功能選單\n或是按下方按鈕\n",
                template=button_template_message
            )
        )          


# In[ ]:


'''
    7.啟動server
    執行此句，啟動Server，觀察後，按左上方塊，停用Server

'''
import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])

