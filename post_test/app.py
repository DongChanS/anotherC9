from flask import Flask,render_template,request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    
    adminEmail = "qwer@qwer.com"
    adminPassword = "12341234"
    
    if email == adminEmail and password == adminPassword:
        msg = "관리자님 환영합니다"
    elif email == adminEmail:
        msg = "관리자님 비밀번호 틀리셨어요"
    else:
        msg = "관리자님 아니시잖아요"
    
    return render_template('signup.html',msg=msg)

app.run()