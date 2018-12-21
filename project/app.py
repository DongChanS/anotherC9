from flask import Flask,render_template,request
import os
import requests
from pprint import pprint as pp
import random

app = Flask(__name__)

token = os.getenv("TOKEN")
naver_id = os.getenv("NAVER_ID")
naver_secret = os.getenv("NAVER_SECRET")

base_url = "https://api.hphk.io/telegram"
my_url = "https://webhook-start666.c9users.io"

@app.route('/{}'.format(token),methods=["POST"])
def telegram():
    doc = request.get_json()
    pp(doc)
    my_id = doc['message']['chat']['id']
    text = doc['message'].get('text')
    img = False
    
    if doc['message'].get('photo') is not None:
        img = True
    
    
    if img:
        file_id = doc.get('message').get('photo')[-1].get('file_id')
        file = requests.get("{}/bot{}/getFile?file_id={}".format(base_url, token, file_id))
        file_url = "{}/file/bot{}/{}".format(base_url, token, file.json().get('result').get('file_path'))
        
        # 네이버로 요청
        res = requests.get(file_url, stream=True)
        clova_res = requests.post('https://openapi.naver.com/v1/vision/celebrity',
            headers={
                'X-Naver-Client-Id':naver_id,
                'X-Naver-Client-Secret':naver_secret
            },
            files={
                'image':res.raw.read()
            })
        if clova_res.json().get('info').get('faceCount'):
            print(clova_res.json().get('faces'))
            text = "{}".format(clova_res.json().get('faces')[0].get('celebrity').get('value'))
        else:
            text = "인식된 사람이 없습니다."
    else:
    	# text 처리
    	text = doc['message']['text']
    
    # if text == "로또":
    #     lotto = str(sorted(random.sample(range(1,46),6)))
    #     reply = lotto + "가 생성되었습니다."
    # else:
    #     reply = text
    chat_url = "{}/bot{}/sendMessage?chat_id={}&text={}".format(base_url,token,my_id,text)
    requests.get(chat_url)
    return '',200


@app.route('/setwebhook')
def setwebhook():
    url = "{}/bot{}/setWebhook?url={}/{}".format(base_url,token,my_url,token)
    print(url)
    res = requests.get(url)
    return ('{}'.format(res), 200)