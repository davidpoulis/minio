from flask import Flask, render_template, request, redirect, url_for
from minio import Minio
from minio.error import S3Error
import random

def upload_to_minio(s3_bucket_name, s3_object_name, object_name):
 try:
    client = Minio(
        "172.17.0.2:9000",
        access_key="Q3AM3UQ867SPQQA43P2F",
        secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
        secure=False,
    )
    found = client.bucket_exists("asiatrip")
    if not found:
        client.make_bucket("asiatrip")
    else:
        print("Bucket " + s3_bucket_name + " already exists")
    client.fput_object(
       s3_bucket_name, s3_object_name, object_name,
    )
    print(
        object_name + " is successfully uploaded as "
        "object "+ s3_bucket_name + "to bucket " + s3_bucket_name
    )
 except S3Error as exc:
  print("error occurred.", exc)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
        file_name = str(random.randint(1000,9999)) + uploaded_file.filename
        upload_to_minio('asiatrip', file_name, uploaded_file.filename)
    return redirect(url_for('index'))