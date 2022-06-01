import os
import sqlalchemy as db
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, json, jsonify
from datetime import datetime

app = Flask(__name__)

load_dotenv() # 讀取 .env 檔案的資料

# 連線 MYSQL
username = os.environ.get("MYSQL_USERNAME")  # 資料庫帳號
password = os.environ.get("MYSQL_PASSWORD")  # 資料庫密碼
host = os.environ.get("MYSQL_DB_ADDRESS")    # 資料庫位址
port = os.environ.get("MYSQL_PORT")  # 資料庫埠號
database = os.environ.get("MYSQL_DB")   # 資料庫名稱

# print(username,password,host,port,database)

# 建立資料庫引擎
engine = db.create_engine(
    f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html',
                           current_time=datetime.utcnow())

@app.route('/module', methods=['GET','POST'])
def module():
    # if request.method == "GET":
    connection = engine.connect()

    cursor = connection.execute("select id,district from district_info3 order by id;")
    result_district = cursor.fetchall()

    # cursor = connection.execute("select DISTINCT Htype from final;")
    # result_htype = cursor.fetchall()

    connection.close()
    if request.method == "GET":
        RRR = 1
        return render_template('module.html',
                                district=result_district,
                                # htype=result_htype,
                                RRR = RRR,
                                modinit = 0,
                                tmpAll = 0,
                                tmpInfo_2021 = 0
                                )
    elif request.method == "POST":
        RRR = 2

        select_mod = request.form['mod']


        if select_mod == "0":
            return render_template('module.html', modinit = 0, RRR = 1, district=result_district, tmpAll = 0, tmpInfo_2021 = 0)

        elif select_mod == "1":

            connection = engine.connect()

            cursor = connection.execute(
                f"select * from district_info2 order by id;") # id | district | real_price | anal_price | diff 
            info_2021 = cursor.fetchall()

            connection.close()

            tmpInfo_2021 = list(map(list,info_2021))

            return render_template('module.html', modinit = 1, RRR = 3, district=result_district, tmpAll = 0, tmpInfo_2021 = tmpInfo_2021)

        elif select_mod == "2":

            select_district = request.form['district']
            
            connection = engine.connect()

            cursor = connection.execute(
                f"select latitude,longitude,address,avg,avg_pred,size from final3 where district_id = '{select_district}';"
                )
            getAll = cursor.fetchall()

            connection.close()

            tmpAll = list(map(list,getAll))

            # tmplen = len(tmpAll)

            return render_template('module.html',
                                    selected_ID = select_district,
                                    district=result_district,
                                    # htype=result_htype,
                                    RRR = RRR,
                                    # tmplen = tmplen,
                                    tmpAll = json.dumps(tmpAll),
                                    modinit = 2,
                                    tmpInfo_2021 = 0
            )

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/analysis_population')
def analysis_population():
    return render_template('analysis_population.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/returnjson', methods=['GET'])
def ReturnJSON():
    if (request.method == 'GET'):
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "./static/towns", "two_towns_all.json")
        data = json.load(open(json_url, encoding="utf-8"))
        return jsonify(data)

if __name__ == "__main__":
    app.run(ssl_context='adhoc',host='0.0.0.0',debug=True, port='7777')
