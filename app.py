from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.8vasl6v.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import datetime

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/today_price')
def today_price():
    update_date = list(db.update_date.find({}, {'_id': False}))

    if len(update_date) == 0 or update_date[0]['date'] != datetime.datetime.now().strftime('%Y/%m/%d'):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        id = "sjasjaruddus@naver.com"
        pwd = "1q2w3e4r!"

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)
        driver.get("https://lostark.game.onstove.com//Market/BookMark")

        time.sleep(0.5)
        elem = driver.find_element(By.XPATH, '//*[@id="user_id"]')
        elem.send_keys(id)
        elem = driver.find_element(By.XPATH, '//*[@id="user_pwd"]')
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)
        time.sleep(0.5)
        elem = driver.find_element(By.XPATH, '// *[ @ id = "itemList"] / thead / tr / th[1] / a').click()
        time.sleep(0.5)

        itemDB = []
        for i in range(0, 9):
            num = str(transform(i))
            xpath = '//*[@id="tbodyItemList"]/tr[' + num + ']/td[1]/div/span[1]/img'
            xpath2 = '//*[@id="tbodyItemList"]/tr[' + num + ']/td[2]/div/em'
            elem1 = driver.find_element(By.XPATH, xpath)
            elem2 = driver.find_element(By.XPATH, xpath2)
            itemDB.append({
                "name": elem1.get_attribute('alt'),
                "price": round(float(elem2.text)),
                "image": elem1.get_attribute('src')
            })

        elem = driver.find_element(By.XPATH,
                                   '//*[@id="lostark-wrapper"]/div/main/div/div[1]/div[1]/div[2]/button').click()
        time.sleep(0.5)
        elem = driver.find_element(By.XPATH, '//*[@id="expand-character-list"]/ul[1]/li[3]/span/button').click()
        time.sleep(0.5)
        elem = driver.find_element(By.XPATH, '//*[@id="modal-info"]/div/div/div[2]/button').click()
        time.sleep(0.5)
        elem = driver.find_element(By.XPATH, '//*[@id="itemList"]/thead/tr/th[1]/a').click()
        time.sleep(0.5)

        for i in range(9, 13):
            num = str(transform(i))
            xpath = '//*[@id="tbodyItemList"]/tr[' + num + ']/td[1]/div/span[1]/img'
            xpath2 = '//*[@id="tbodyItemList"]/tr[' + num + ']/td[2]/div/em'
            elem1 = driver.find_element(By.XPATH, xpath)
            elem2 = driver.find_element(By.XPATH, xpath2)
            itemDB.append({
                "name": elem1.get_attribute('alt'),
                "price": round(float(elem2.text)),
                "image": elem1.get_attribute('src')
            })

        elem = driver.find_element(By.XPATH,
                                   '//*[@id="lostark-wrapper"]/div/main/div/div[1]/div[1]/div[2]/button').click()
        time.sleep(0.5)
        elem = driver.find_element(By.XPATH, '//*[@id="expand-character-list"]/ul[1]/li[1]/span/button').click()
        driver.close()

        doc = {}
        doc["date"] = datetime.datetime.now().strftime('%Y/%m/%d')

        db.update_date.delete_many({})
        db.update_date.insert_one(doc)

        db.itemDB.delete_many({})
        db.itemDB.insert_many(itemDB)

    itemDB = list(db.itemDB.find({}, {"_id": False}))
    crystal = list(db.crystal.find({}, {"_id": False}))

    return jsonify({"daily_price": itemDB,
                    "crystal": crystal})

@app.route("/save_user", methods=["POST"])
def save_user():
    user_data = request.form.getlist('data_give[]')
    print(user_data)
    user = db.user_data.find_one({'0': user_data[0]})
    msg = '영지 정보 저장 완료'

    print(user)
    if user is not None:
        db.user_data.delete_one({'0': user_data[0]})
        msg = '영지 정보 수정 완료'

    doc = {
        '0': user_data[0],
        '1': user_data[1],
        '2': user_data[2],
        '3': user_data[3],
        '4': user_data[4]
    }

    db.user_data.insert_one(doc)
    return jsonify({"msg": msg})

@app.route("/load_user", methods=["POST"])
def load_user():
    data_receive = request.form['data_give']
    user_data = list(db.user_data.find({'0': data_receive}, {'_id': False}))
    print(user_data)
    if len(user_data) == 1:
        return jsonify({"user_data": user_data})
    else:
        return jsonify({"user_data": "해당 닉네임으로 저장된 영지 정보가 없습니다."})

@app.route("/crawling", methods=["GET"])
def crawling():
    id = "sjasjaruddus@naver.com"
    pwd = "1q2w3e4r!"

    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)
    driver.get("https://lostark.game.onstove.com/Market/BookMark")

    time.sleep(0.5)
    elem = driver.find_element(By.XPATH, '//*[@id="user_id"]')
    elem.send_keys(id)
    elem = driver.find_element(By.XPATH, '//*[@id="user_pwd"]')
    elem.send_keys(pwd)
    elem.send_keys(Keys.RETURN)
    time.sleep(0.5)
    elem = driver.find_element(By.XPATH, '// *[ @ id = "itemList"] / thead / tr / th[1] / a').click()
    time.sleep(0.5)

    price_list = [0] * 9
    for i in range(0, 9):
        num = str(transform(i))
        xpath2 = '//*[@id="tbodyItemList"]/tr[' + num + ']/td[4]/div/em'
        elem2 = driver.find_element(By.XPATH, xpath2)
        price_list[i] = elem2.text

    return jsonify({"price_list": price_list})

@app.route("/save_crystal", methods=["POST"])
def save_crystal():
    data_receive = request.form["data_give"]
    print(data_receive)
    doc = {
        "crystal": data_receive
    }

    db.crystal.delete_many({})
    db.crystal.insert_one(doc)
    return jsonify({"msg": "msg"})

def transform(num):
    if num == 0:
        return 1
    if num == 1:
        return 6
    if num == 2:
        return 7
    if num == 3:
        return 2
    if num == 4:
        return 5
    if num == 5:
        return 8
    if num == 6:
        return 3
    if num == 7:
        return 4
    if num == 8:
        return 9
    if num == 9:
        return 4
    if num == 10:
        return 3
    if num == 11:
        return 1
    if num == 12:
        return 2

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
