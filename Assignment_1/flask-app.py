#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for
import boto3

app = Flask(__name__)
s3 = boto3.resource('s3')


def return_buckets():
    buckets = []
    for bucket in s3.buckets.all():
        buckets.append(bucket.name)
    return buckets


def return_folders(bucket):
    folders = []
    bucket = s3.Bucket(bucket)
    result = bucket.meta.client.list_objects(Bucket=bucket.name, Delimiter='/')
    for output in result.get('CommonPrefixes'):
        folders.append(output.get('Prefix'))
    return folders


def return_files(bucket, folder):
    bucket = s3.Bucket(bucket)
    file_list = list(bucket.objects.filter(Prefix=folder))
    return file_list[1:]


@app.route('/')
def index():
    buckets = return_buckets()
    return render_template('index.html', buckets=buckets)


@app.route('/bucket/<string:bucket>', methods=['GET', 'POST'])
def folders(bucket):
    if request.method == 'GET':
        folders = return_folders(bucket)
        return render_template('folders.html', bucket=bucket, folders=folders)


@app.route('/bucket/<string:bucket>/<string:folder>/', methods=['GET', 'POST'])
def files(bucket, folder):
    if request.method == 'GET':
        files = return_files(bucket, folder)
    return render_template('files.html', files=files)


if __name__ == '__main__':
    app.run(debug=True, port=8085)
