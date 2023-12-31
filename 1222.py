import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
collection_ref = db.collection("小說")
docs = collection_ref.get()
found = False
info = ""
for doc in docs:                                                                                                                
    book_dict = doc.to_dict()
    keyword = "的的"
    if keyword in book_dict["title"]:
        found = True 
        info += "書名：" + book_dict.get("title", "N/A") + "\n"
        info += "封面：" + book_dict.get("picture", "N/A") + "\n"
        info += "書籍連結：" + book_dict.get("hyperlink", "N/A") + "\n"

if not found:
    info += "很抱歉，目前無符合這個關鍵字的相關小說喔"
print(info)

