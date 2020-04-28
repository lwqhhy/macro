from flask import Flask, request, render_template, jsonify
import pymysql
import sys
import json
import decimal
import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World 2 !'

def get_dbmysql():
    db = pymysql.connect('localhost', 'root', 'yadan', 'collect_db', charset="utf8")
    return db

#查询mysql带字段名返回
def query_dbmysql_name(query, args=(), one=False):
    db = get_dbmysql()
    cur = db.cursor(pymysql.cursors.DictCursor)
    res = cur.execute(query)
    rv = cur.fetchall()
    db.close()
    return (rv[0] if rv else None) if one else rv

#查询mysql不带字段名
def query_dbmysql(query, args=(), one=False):
    db = get_dbmysql()
    cur = db.cursor()
    res = cur.execute(query)
    db.commit()
    rv = cur.fetchall()
    db.close()
    return (rv[0] if rv else None) if one else rv
#测试接口
@app.route("/HELLO", methods=["GET"])
def GET_HELLO():
    if request.method == "GET":
      result = "{'code':0,'msg':'执行成功'}"
    return result

#POST接口获取指定日期的宏观控制图点数据
@app.route("/MACRO_CHART", methods=["POST"])
def MACRO_CHART():
    if request.method == "POST":
        dto = request.form['reqdate']
        res = query_dbmysql_name("SELECT well_no,bx,pump_inlet_press FROM pd_well_macro_daily where date_format(prod_date,'%Y%m%d')='"+ dto + "'")

    data = json.dumps(res, cls=DecimalEncoder)
    result = "{'code':0,'msg':'执行成功','data':" + data + "}"
    return result

#取得宏观控制图参数
@app.route("/GET_PARAM", methods=["GET"])
def GET_PARAM():
    if request.method == "GET":
        res = query_dbmysql_name("SELECT max_pumpe,min_pumpe,max_press,min_press FROM PD_MACRO_SET where org_id='957DA301E8F64933BBCA33E2AE001DDC'")
    data = json.dumps(res, cls=DecimalEncoder)
    result = "{'code':0,'msg':'执行成功','data':" + data + "}"
    return result

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        super(DecimalEncoder, self).default(o)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
