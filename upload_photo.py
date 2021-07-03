from flask.globals import request, session
from main import db_RDS
import boto3
from flask import Blueprint,request,jsonify
from config import aws_access_key_id,aws_secret_access_key

s3 = boto3.client(
    "s3",
    aws_access_key_id = aws_access_key_id,
    aws_secret_access_key = aws_secret_access_key
)

upload_photo_app = Blueprint("upload_photo_app",__name__)

allow_path = set(["jpg","png","JPG","PNG"])

@upload_photo_app.route("/api/user_photo",methods=["POST"])
def upload():
    if request.method=="POST":
        photo = request.files["files"]
        if photo.filename.split(".")[-1] not in allow_path:
            return jsonify({"error":True})
        email = session.get("email")
        real_path = "http://d3nczlg85bnjib.cloudfront.net/"+photo.filename
        sql = f"UPDATE attraction.user SET img_src = '{real_path}' WHERE email = '{email}'"
        db_RDS.engine.execute(sql)
        ##photo.save(file_path)
        s3.upload_fileobj(photo,"tonytony58",photo.filename,ExtraArgs={'ACL': 'public-read'})
        return jsonify({"ok":True})