from flask import Flask, redirect, render_template, session, url_for, request, jsonify
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from webmodel import db, Attraction
import json
import collections


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False

load_dotenv()

host = os.getenv('host')
username = os.getenv('username')
password = os.getenv('password')
database = os.getenv('database')
# print(host,username,password,database)

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{username}:{password}@{host}:3306/{database}"

db.init_app(app)

# 景點數量
total_attractions_num = 319
# 一頁的數量
onepage_num = 12

# 錯誤訊息
error_message = {
	"1":"景點編號不正確",
	"2":"伺服器內部錯誤，請稍後再試",
	"3":"頁數錯誤",
}


# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


@app.route("/api/attractions")
def attractions_api():
	'''
	依照關鍵字查詢，若無為全部
	指定頁數的景點列表
	'''
	try:
		page = int(request.args.get("page"))
		keyword = request.args.get("keyword")
		begin = page * onepage_num
		if keyword != None:
			name_keyword = "%{}%".format(keyword)
			query_num = Attraction.query.filter(Attraction.name.like(name_keyword)).count()
			if begin < query_num:
				end, nextpage = pagecheck(query_num, page, begin)
				query = Attraction.query.filter(Attraction.name.like(name_keyword)).limit(end).offset(begin).all()
				res, state = onepage_json(query, nextpage, end)
			else:
				# 代表超過頁數
				res = error_json(error_message["3"])
				state = 500
		else:
			query_num = Attraction.query.count()
			if begin < query_num:
				end, nextpage = pagecheck(query_num, page, begin)
				query = Attraction.query.limit(end).offset(begin).all()
				res, state = onepage_json(query, nextpage, end)
			else:
				# 代表超過頁數
				res = error_json(error_message["3"])
				state = 500
		return jsonify(res), state
	except:
		res = error_json(error_message["2"])
		state = 500
		return jsonify(res), state


@app.route("/api/attraction/<int:id>")
def attraction_query(id):
	'''
	依照 id 查詢景點
	'''
	try:
		if id <= total_attractions_num and id > 0:
			query = Attraction.query.filter_by(id=id).first()
			att_data = attraction_json(query)
			res = {
				"data":att_data
			}
			state = 200
		else:
			res = error_json(error_message["1"])
			state = 400

		return jsonify(res), state
	except:
		res = error_json(error_message["2"])
		state = 500

		return jsonify(res), state


def pagecheck(query_num, page, begin):
	'''
	確認頁數範圍及是否有下一頁
	'''
	check = (page + 1) * onepage_num
	if check > query_num:
		end = query_num % onepage_num
		nextpage = None
	else:
		end = onepage_num
		nextpage = page + 1

	return end, nextpage


def onepage_json(query, nextpage, end):
	'''
	此頁的景點資料 JSON
	'''
	data = []
	for i in range(end):
		att_data = attraction_json(query[i])
		data.append(att_data)
	res = {
		"nextPage": nextpage,
		"data": data
	}
	state = 200
	
	return res, state


def attraction_json(data):
	'''
	景點資料 JSON
	'''
	# att_form = collections.OrderedDict()
	att_form = {}
	att_form["id"] = data.id
	att_form["name"] = data.name
	att_form["category"] = data.category
	att_form["description"] = data.description
	att_form["address"] = data.address
	att_form["transport"] = data.transport
	att_form["mrt"] = data.mrt
	att_form["latitude"] = data.latitude
	att_form["longitude"] = data.longitude
	att_form["images"] = eval(data.images)
	
	return att_form


def error_json(error_message):
	'''
	錯誤訊息 JSON
	'''
	res = {
		"error": True,
		"message": error_message
	}
	return res


if __name__ == "__main__":
	app.run(host="0.0.0.0",port=3000)