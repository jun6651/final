@app.route("/webhook4", methods=["POST"])
def webhook4():
    req = request.get_json(force=True)
    action =  req["queryResult"]["action"]
    if (action == "BookDetail"): #book intent action&parameters
        keyword =  req.get("queryResult").get("parameters").get("any") 
        info = "我是小說聊天機器人，您要查詢關鍵字是" + keyword + "的小說\n\n"
    
    db = firestore.client()
    collection_ref = db.collection("小說")
    docs = collection_ref.get()
    Found = False
    info = ""
    for doc in docs:                                                                                                                
        dict = doc.to_dict()
        if keyword in dict["keyword"]:
            found = True 
            info += "書名：" + dict["title"] + "\n"
            info += "封面：" + dict["picture"] + "\n"
            info += "書籍連結：" + dict["hyperlink"] + "\n"
        if not found:
            info += "很抱歉，目前無符合這個關鍵字的相關小說喔"

        
    return make_response(jsonify({"fulfillmentText": info}))



        db = firestore.client()
        collection_ref = db.collection("小說")
        docs = collection_ref.get()
        found = False
        info = ""
        for doc in docs:                                                                                                                
            book_dict = doc.to_dict()
            if keyword in book_dict["keyword"]:
                found = True 
                info += "書名：" + book_dict.get("title", "N/A") + "\n"
                info += "封面：" + book_dict.get("picture", "N/A") + "\n"
                info += "書籍連結：" + book_dict.get("hyperlink", "N/A") + "\n"

        if not found:
            info += "很抱歉，目前無符合這個關鍵字的相關小說喔"