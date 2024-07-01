import functions_framework
from google.cloud import firestore

db = firestore.Client()

@functions_framework.http
def get_book(request):
    try:
        book_id = request.args.get('id')
        book_ref = db.collection('books').document(book_id)
        book = book_ref.get()
        if book.exists:
            return book.to_dict(), 200
        else:
            return 'Book not found', 404
    except Exception as e:
        return str(e), 500
