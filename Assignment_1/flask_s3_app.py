from flask import jsonify,request,make_response,Flask
import boto3

app = Flask("__name__")
s3 = boto3.resource('s3')

@app.route("/get_s3_filenames",methods=["GET"])
def filename():
    output = []
    for bucket in s3.buckets.all():
        output.append(bucket.name)
        for key in bucket.objects.all():
            output.append(key.key)
    html = ""
    for item in output:
	    html += "<br>"+item+"</br>"
    return html

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=False,port=8085,use_reloader=False)
