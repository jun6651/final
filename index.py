from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)

@app.route("/")
def index():
    x ="作者-林映均12/17<br>"
    x +="<a href=/webhook4>資管導論</a><br>"
    return x

@app.route("/spider2")
def spider2():
    info = ""
    url = "https://www.xbanxia.com/list/10_1.html"
    Data = requests.get(url)
    Data.encoding = "utf-8"
    #print(Data.text)
    sp = BeautifulSoup(Data.text, "html.parser")
    result=sp.select(".pop-book2")

    for x in result:
            info += "<a href=" + x.find("a").get("href") + ">" + x.find("h2").text + "</a><br>"
            info += x.find("a").get("href") + "<br>"
            info += "<img src=https://www.xbanxia.com/" + x.find("img").get("src") + " width=200 height=300 " + "</img><br>"
    return info


@app.route("/book")
def book():
    url = "https://www.xbanxia.com/list/10_1.html"  
    Data = requests.get(url)
    Data.encoding = "utf-8"
    sp = BeautifulSoup(Data.text, "html.parser")
    result=sp.select(".pop-book2")  #是否正確
    info = ""
    for item in result:
      picture = item.find("img").get("src").replace(" ", "")
      title = item.find("h2").text
      book_id = item.find("a").get("href").replace("/", "").replace("book", "")
      hyperlink = "https://www.xbanxia.com/list/10_1.html" + item.find("a").get("href")
      info += picture + "\n" + title +"\n"+ hyperlink +"\n" 
      doc = {
          "title": title,
          "picture": picture,
          "hyperlink": hyperlink,
      }

      db = firestore.client()
      doc_ref = db.collection("小說").document(book_id)
      doc_ref.set(doc)
    return "近期上映小說已爬蟲及存檔完畢"
               

@app.route("/webhook4", methods=["POST"])
def webhook4():
    req = request.get_json(force=True)
    action = req["queryResult"]["action"]
    if action == "BookDetail":  # book intent action&parameters
        keyword = req.get("queryResult").get("parameters").get("any")
        info = "我是小說聊天機器人，您要查詢關鍵字是" + keyword + "的小說\n\n"
        db = firestore.client()
        collection_ref = db.collection("小說")
        docs = collection_ref.get()
        found = False
        info = ""
        for doc in docs:                                                                                                                
            book_dict = doc.to_dict()
            if keyword in book_dict["title"]:
                found = True 
                info += "書名：" + book_dict.get("title", "N/A") + "\n"
                info += "封面：" + book_dict.get("picture", "N/A") + "\n"
                info += "書籍連結：" + book_dict.get("hyperlink", "N/A") + "\n"

        if not found:
            info += "很抱歉，目前無符合這個關鍵字的相關小說喔"

    return make_response(jsonify({"fulfillmentText": info}))
   


#if __name__ == "__main__":
#    app.run(debug=True)
