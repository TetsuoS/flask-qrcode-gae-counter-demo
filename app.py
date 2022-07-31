# ワンタイムURLサンプルプログラム
# 必要パッケージ）
# pip3 install flask uuid
# 実行方法）
# FLASK_ENV=development flask run

from flask import Flask
from flask.templating import render_template, render_template_string
from flask import jsonify, request
import uuid
import time
import os
import json
import datetime
from PIL import Image, ImageDraw, ImageFont

# QRコード機能追加用
import qrcode
import base64
from io import BytesIO

# カウンター
def inc_counter():
    is_file = os.path.exists(r"count.txt")
    if not is_file:
        f = open('./count.txt', 'w')
        f.write('0')
        f.close()
    with open('./count.txt', 'r+') as f:
        data = f.read()
        counter = int(data)
        counter += 1
        new_count = str(counter)
        f.seek(0)
        f.write(new_count)
        return new_count

app = Flask(__name__)

storage_path = '/tmp/'  # ローカル環境でWindowsの場合は ./storage/
expire_time = 3600  # URLの生存時間（秒）

# カウンター
"""
def getSize(txt, font):
    testImg = Image.new('RGB', (1, 1))
    testDraw = ImageDraw.Draw(testImg)
    return testDraw.textsize(txt, font)

fontname = "Arial.ttf"
fontsize = 11
text = "1"

colorText = "black"
colorOutline = "red"
colorBackground = "white"

font = ImageFont.truetype(fontname, fontsize)
width, height = getSize(text, font)
img_counter = Image.new('RGB', (width+4, height+4), colorBackground)
d = ImageDraw.Draw(img_counter)
d.text((2, height/2), text, fill=colorText, font=font)
d.rectangle((0, 0, width+3, height+3), outline=colorOutline)
db_buffer = BytesIO(img_counter)
img_counter.save(db_buffer, format="png")
#img_dkm.save("suuji.png")
"""


# トップディレクトリ
@app.route('/', methods=['GET', 'POST'])
def home():
    # ユニークIDの作成
    id = str(uuid.uuid4())
    app.logger.debug(id + ' is generated and check /q/' + id + '/' + id)

    # idに紐付くデータ作成
    current_message = 'このQRコードは ' + str(datetime.datetime.now()) + ' に作成されました。'

    data = {
        'expire_at': time.time() + expire_time,  # 有効期限を設定
        'text': current_message  # QRコードで渡されるメッセージ
    }

    # データを一時領域にidのファイル名で保存
    path = storage_path + id
    with open(path, 'w') as f:
        f.write(json.dumps(data))

    # QRコードの作成
    # QRコード画像の作成
    # img = qrcode.make(id)
    qr = qrcode.QRCode(
        box_size = 4,
        border = 8,
        version = 12,
        error_correction = qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(id)
    qr.make()
    #img = qr.make_image()


    # 画像を表示するためにbase64形式に変換する
    buffer = BytesIO()
    img = qr.make_image(fill_color="red", back_color="#23dda0")
    #img.save(buffer, format="png")

    # ロゴイメージ
    logo = Image.open('./dkm.png').resize((30,30))
    pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
    img.paste(logo, pos)
    img.save(buffer, format="png")
    img_encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    #img_encoded_counter = base64.b64encode(img_counter.getvalue().decode("ascii"))

    # カウンター
    counter = inc_counter()

    # 発行URLのQRコード表示画面
    return render_template('qrcode.html', img_encoded=img_encoded, id=id, counter=counter) #img_encoded_counter=img_encoded_counter)
