import requests

def print_book(book):
    print('Book {')
    for key in book.keys():
        attr = str(key)
        val = str(book[key])
        print("\t" + attr + ":" + val)
    print('}')

def get_book(id):
    r = requests.get("http://127.0.0.1:8888/books/" + str(id))
    book = r.json()
    print("Get status Code:" + str(r.status_code))
    if r.ok:
        print_book(book)
        return book
    else:
        print('Error:' + book['message'])

if __name__=="__main__":
    print("=======Book info before update=========")
    book = get_book(206)

    print("=======Update Book Info================")
    book['Author'] = 'Nobody'
    r = requests.put("http://127.0.0.1:8888/books/206", json=book)
    print("Get status Code:" + str(r.status_code))
    print(r.json()['message'])

    print("========Book Info after update=========")
    book = get_book(206)