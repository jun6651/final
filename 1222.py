
            db = firestore.client()
            collection_ref = db.collection("小說")
            docs = collection_ref.get()
            Found = False
            info = ""
            for doc in docs:                                                                                                                
                dict = doc.to_dict()
                if keyword in dict["title"]:
                    found = True 
                    info += "書名：" + dict["title"] + "\n"
                    info += "封面：" + dict["picture"] + "\n"
                    info += "書籍連結：" + dict["hyperlink"] + "\n"
            if not found:
                info += "很抱歉，目前無符合這個關鍵字的相關電影喔"