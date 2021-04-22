import json
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('host')
username = os.getenv('username')
password = os.getenv('password')
database = os.getenv('database')

tabel = 'attraction_data'
print(host,username,password,database)


Connection = pymysql.connect(host=host, user=username, password=password, db=database, cursorclass=pymysql.cursors.DictCursor)
# cursor = Connection.cursor()


def sql_up(data):
    sql = "INSERT INTO {} (rowid,name,category,description,address,transport,mrt,latitude,longitude,images) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(tabel)
    cursor.execute(sql,data)

def sql_up_many(data):
    sql = "INSERT INTO {} (rowid,name,category,description,address,transport,mrt,latitude,longitude,images) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(tabel)
    cursor.executemany(sql,data)

def data_report(data):
    rowid = data["_id"]
    name = data["stitle"]
    category = data["CAT2"]
    description = data["xbody"]
    address = data["address"]
    if data["info"] == None:
        transport = ""
    else:
        transport = data["info"]
    if data["MRT"] == None:
        mrt = ""
    else:
        mrt = data["MRT"]
    latitude = float(data["latitude"])
    longitude = float(data["longitude"])
    images = str(img_renew(data["file"]))
    print(len(images))
    report = (rowid,name,category,description,address,transport,mrt,latitude,longitude,images)
    return report

def img_renew(img):
    imgcheck = ["jpg","png"]
    img = img.split("http://")
    new_img = []
    for i in img:
        imgfile = i.split(".")[-1]
        if imgfile.lower() in imgcheck:
            new_img.append(i.replace("www","http://www"))
    print(new_img)
    return new_img

with open ("taipei.json","r", encoding="utf-8") as f:
    data = json.load(f)
    data = data["result"]["results"]
    print(len(data))
    new = []
    for i in range(len(data)):
        for d in data:
            if d["_id"] == i+1:
                new.append(d)

new_report = []
for n in range(len(new)):
    report = data_report(new[n])
    new_report.append(report)
    # == sql_up
    # with Connection.cursor() as cursor:
    #     sql_up(report)
    #     cursor.close()
    # Connection.commit()
    # ==

# == sql_up_many
with Connection.cursor() as cursor:
    sql_up_many(new_report)
    cursor.close()
Connection.commit()
# ==


# cursor.close()
# Connection.commit()
