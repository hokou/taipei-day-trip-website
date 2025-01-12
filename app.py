from flask import Flask, redirect, render_template, session, url_for, request, jsonify
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from webmodel import db, Attraction, User, Order
import json
import collections
from datetime import datetime
import requests


app = Flask(__name__,
            static_folder="static",
            static_url_path="/")
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False

load_dotenv()

host = os.getenv('host')
username = os.getenv('username')
password = os.getenv('password')
database = os.getenv('database')
secretkey = os.getenv('secretkey')
PartnerKey = os.getenv('PartnerKey')
MerchantID = os.getenv('MerchantID')

# print(host,username,password,database)
app.secret_key = secretkey.encode(encoding="utf-8")
# print(app.secret_key)

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
	"4":"查無資料",
	"5":"帳號或密碼錯誤",
    "6":"帳號已經被註冊",
    "7":"輸入資料錯誤，請重新註冊",
    "8":"輸入資料錯誤，請重新登入",
	"9":"請先登出",
	"10":"請先登入",
	"11":"訂單更新失敗"
}

order_message = {
	"0":"付款成功",
	"1":"付款失敗",
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


# attraction
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
			# print("check", name_keyword, query_num)
			if begin < query_num:
				end, nextpage = pagecheck(query_num, page)
				query = Attraction.query.filter(Attraction.name.like(name_keyword)).limit(end).offset(begin).all()
				res, state = onepage_json(query, nextpage, end)
			else:
				# 代表查無資料
				res = error_json(error_message["4"])
				state = 500
		else:
			query_num = Attraction.query.count()
			if begin < query_num:
				end, nextpage = pagecheck(query_num, page)
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


def pagecheck(query_num, page):
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


# test data
# data = {
# 	"id": 1,
# 	"name": "ply",
# 	"email": "ply@ply.com",
# 	"password": "12345678"
# }


# user
@app.route("/api/user", methods=["GET"])
def user_get():
	if request.method == "GET":
		# session["id"] = 1
		# session.clear()
		if "id" in session:
			print("OK")
			data = {
				"id": session["id"],
				"name": session["name"],
				"email": session["email"]
			}
			res = user_json(data)
			state = 200
		else:
			res = { 
				"data": None
			}
			state = 200
	
	return jsonify(res), state


@app.route("/api/user", methods=["POST"])
def user_signup():
	if request.method == "POST":
		try:
			user_data = request.get_json()
			name = user_data['name']
			email = user_data['email']
			password = user_data['password']
			if "id" in session:
				res = error_json(error_message["9"])
				state = 400
				return jsonify(res), state
			if name == None or email == None or password == None:
				res = error_json(error_message["7"])
				state = 400
				return jsonify(res), state
			else:
				query = User.query.filter_by(email=email).first()
				print("query",query)
				if query != None:
					res = error_json(error_message["6"])
					state = 400
					return jsonify(res), state
				else:
					signup_data = User(name=name, email=email, password=password)
					db.session.add(signup_data)
					db.session.commit()
					print("signup ok")
					res = {
						"ok": True
					}
					state = 200
					return jsonify(res), state
		except Exception as e:
			print(e)
			res = error_json(error_message["2"])
			state = 500
			return jsonify(res), state


@app.route("/api/user", methods=["PATCH"])
def user_login():
	if request.method == "PATCH":
		try:
			user_data = request.get_json()
			email = user_data['email']
			password = user_data['password']
			if "id" in session:
				res = error_json(error_message["9"])
				state = 400
				return jsonify(res), state
			if email == None or password == None:
				res = error_json(error_message["8"])
				state = 400
				return jsonify(res), state
			else:
				query = User.query.filter_by(email=email).first()
				print("query",query)
				if query == None:
					res = error_json(error_message["5"])
					state = 400
					return jsonify(res), state
				elif email != query.email or password != query.password:
					res = error_json(error_message["5"])
					state = 400
					return jsonify(res), state
				elif email == query.email and password == query.password:
					session["id"] = query.id
					session["name"] = query.name
					session["email"] = query.email
					res = {
						"ok": True
					}
					state = 200
					return jsonify(res), state
		except Exception as e:
			print(e)
			res = error_json(error_message["2"])
			state = 500
			return jsonify(res), state


@app.route("/api/user", methods=["DELETE"])
def user_logout():
	if request.method == "DELETE":
		session.pop("id", None)
		session.pop("name", None)
		session.pop("email", None)
		# session.pop("password", None)
		session.clear()
		res = {
			"ok": True
		}
		state = 200
	
	return jsonify(res), state


def user_json (data):
	user_mess = {
		"data": data
	}
	print(user_mess)
	return user_mess


# booking
@app.route("/api/booking", methods=["GET"])
def booking_get():
	if request.method == "GET":
		# if "id" in session:
		# 	if "booking_data" in session:
		# 		booking_dict = session["booking_data"]
		# 		print("---------",booking_dict)
		# 		booking_dict = dict(booking_dict)
		# 		print("---------",booking_dict)
		# 		attractionId = booking_dict["attractionId"]
		# 		query = Attraction.query.filter_by(id=attractionId).first()
		# 		res = booking_JSON(booking_dict, query)
		# 		state = 200
		try:
			if "id" in session:
				if "booking_data" in session:
					booking_dict = session["booking_data"]
					booking_dict = dict(booking_dict)
					attractionId = booking_dict["attractionId"]
					query = Attraction.query.filter_by(id=attractionId).first()
					res = booking_JSON(booking_dict, query)
					state = 200
				else:
					res = {
						"data": None
					}
					state = 200
			else:
				res = error_json(error_message["10"])
				state = 400

		except Exception as e:
			print(e)
			res = error_json(error_message["2"])
			state = 500
	
		return jsonify(res), state


@app.route("/api/booking", methods=["POST"])
def booking_new():
	if request.method == "POST":
		try:
			if "id" in session:
				booking_data = request.get_json()
				session["booking_data"] = booking_data
				res = {
					"ok": True
				}
				state = 200
			else:
				res = error_json(error_message["10"])
				state = 400

		except Exception as e:
			print(e)
			res = error_json(error_message["2"])
			state = 500
	
		return jsonify(res), state


@app.route("/api/booking", methods=["DELETE"])
def booking_delect():
	if request.method == "DELETE":
		try:
			if "id" in session:
				session.pop("booking_data", None)
				res = {
					"ok": True
				}
				state = 200
			else:
				res = error_json(error_message["10"])
				state = 200
		except Exception as e:
			print(e)
			res = error_json(error_message["2"])
			state = 500
	
		return jsonify(res), state


def booking_JSON(booking_dict, query):
	images = eval(query.images)
	data = {
		"data": {
			"attraction": {
				"id": query.id,
				"name": query.name,
				"address": query.address,
				"image": images[0]
			},
			"date": booking_dict["date"],
			"time": booking_dict["time"],
			"price": booking_dict["price"]
			}
	}
	return data


# order
@app.route("/api/order/<orderNumber>", methods=["GET"])
def order_get(orderNumber):
	if request.method == "GET":
		try:
			if "id" in session:
				query = Order.query.filter_by(order_number=orderNumber).first()
				if query != None:
					res = order_JSON(query)
					state = 200
				else:
					res = {
						"data": None
					}
					state = 200
			else:
				res = error_json(error_message["10"])
				state = 400

		except Exception as e:
			print(e)
			res = error_json(error_message["2"])
			state = 500
	
		return jsonify(res), state


@app.route("/api/orders", methods=["POST"])
def order_post():
	if request.method == "POST":
		try:
			if "id" in session:
				order_data = request.get_json()
				session["order_data"] = order_data
				time = datetime.now()
				user_id = session["id"]
				order_number = order_num(time, user_id)
				# 代表未付款
				order_status = 1
				order_add(order_data, user_id, order_number, order_status)
				req = order_to_tappay(order_data)
				order_status = int(req["status"])
				if order_status == 0:
					order_mes = order_message["0"]
					ret = order_change(order_number, order_status)
					if ret != True:
						res = error_json(error_message["11"])
						state = 400
						return jsonify(res), state
				else:
					order_mes = order_message["1"]
				
				res = {
					"data": {
						"number": order_number,
						"payment": {
							"status": order_status,
							"message": order_mes
						}
					}
				}
				state = 200
			else:
				res = error_json(error_message["10"])
				state = 400

		except Exception as e:
			print(e)
			res = error_json(error_message["2"])
			state = 500
	
		return jsonify(res), state


def order_add(data, user_id, order_number, order_status):
	order = data["order"]
	trip = order["trip"]
	contact = data["contact"]
	order_data = Order(user_id=user_id, order_number=order_number, order_price=order["price"], order_status=order_status, 
						trip_id=trip["attraction"]["id"], trip_date=trip["date"], trip_time=trip["time"], 
						contact_name=contact["name"], contact_email=contact["email"], contact_phone=contact["phone"])
	db.session.add(order_data)
	db.session.commit()
	print("order add ok")


def order_change(order_number, order_status):
	try:
		query = Order.query.filter_by(order_number=order_number).first()
		query.order_status = order_status
		db.session.commit()
		return True
	except:
		return False

def order_to_tappay(order_data):
	prime = order_data["prime"]
	order = order_data["order"]
	contact = order_data["contact"]
	tappay_url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
	request_headers = {
		"Content-Type": "application/json", 
		"x-api-key": PartnerKey
	}

	request_body = {
		"prime": prime,
		"partner_key": PartnerKey,
		"merchant_id": MerchantID,
		"details":"TapPay Test",
		"amount": order["price"],
		"cardholder": {
			"name": contact["name"],
			"email": contact["email"],
			"phone_number": contact["phone"],
		},
		"remember": True
	}

	request = requests.post(tappay_url, headers=request_headers, data=json.dumps(request_body, ensure_ascii=False).encode('utf8') )
	req =request.json()

	return req


def order_num(time, id):
	now_time = time.strftime("%Y%m%d%H%M%S")
	id_num = str(id).zfill(5)
	order_number = f"{now_time}{id_num}"
	return order_number


def order_JSON(query):
	attraction_query = Attraction.query.filter_by(rowid=query.trip_id).first()
	attraction_images = eval(attraction_query.images)

	data = {
		"data": {
			"number": query.order_number,
			"price": query.order_price,
			"trip": {
				"attraction": {
					"id": query.trip_id,
					"name": attraction_query.name,
					"address": attraction_query.address,
					"image": attraction_images[0]
				},
			"date": query.trip_date,
			"time": query.trip_time
			},
			"contact": {
			"name": query.contact_name,
			"email": query.contact_email,
			"phone": query.contact_phone
			},
			"status": query.order_status
		}
	}
	return data


if __name__ == "__main__":
	app.run(host="0.0.0.0",port=3000)