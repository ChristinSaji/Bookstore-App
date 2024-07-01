import functions_framework
from google.cloud import firestore

db = firestore.Client()

@functions_framework.http
def add_book(request):
    try:
        data = request.get_json()
        book_id = data['id']
        db.collection('books').document(book_id).set(data)
        return 'Book added successfully', 200
    except Exception as e:
        return str(e), 500
