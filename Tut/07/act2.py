import requests

if __name__=="__main__":
    book = {
                "Date_of_Publication": 0,
                "Publisher": "string",
                "Author": "string",
                "Title": "string",
                "Flickr_URL": "string",
                "Identifier": 0,
                "Place_of_Publication": "string"
            }
    
    r = requests.post("http://127.0.0.1:8888/books", json=book)

    print("Status Code:" + str(r.status_code))
    resp = r.json()

    print(resp['message'])
