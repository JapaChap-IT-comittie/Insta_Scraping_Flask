from flask import Flask
from flask import render_template,request,send_file
import api,os
import pandas as pd
# create the app
app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    with app.app_context():
        if request.method == "GET":
            return render_template("index.html")
        elif request.method == "POST":
            if request.form["button"]  == "Fetch":
                print("qrick fetch data")
                shortURL = request.form.get("short")
                print(shortURL)
                try:
                    df = api.scrape(shortURL)
                    header = df.columns
                    record = df.values.tolist()
                    message="Successes to fetch the data"
                    return render_template("index.html", header = header, record=record,message=message)
                except:
                    import traceback
                    traceback.print_exc()
                    message = "We couldn't find the page. Try again."
                    return render_template("index.html", message = message)
            elif request.form["button"] == "CSV":
                try:
                    downloadFile = f"{os.getcwd()}/data.csv"
                    return send_file(downloadFile,as_attachment = True)
                except:
                    message = "You can't download the CSV file because the data is empty now "
                    return render_template("index.html", message = message)
            elif request.form["button"] == "Read":
                try:
                    df = api.readCSV("data.csv")
                    header = df.columns
                    record = df.values.tolist()
                    return render_template("index.html", header = header, record = record)
                except:
                    message = "The table is empty now"
                    return render_template("index.html",message = message)

            elif request.form["button"] == "Delete":
                try:
                    os.remove("data.csv")
                    message = "Success to delete table"
                except:
                    message = "Already deleted"
                return render_template("index.html",message = message)







