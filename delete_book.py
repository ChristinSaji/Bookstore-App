import functions_framework
from google.cloud import firestore, storage

db = firestore.Client()
storage_client = storage.Client()
bucket_name = 'book-cover-image'
bucket = storage_client.bucket(bucket_name)

@functions_framework.http
def delete_book(request):
    try:
        book_id = request.args.get('id')
        book_ref = db.collection('books').document(book_id)
        book = book_ref.get()
        if book.exists:
            book_data = book.to_dict()
            book_ref.delete()

            # If the document contains a cover image URL, delete the corresponding file from Cloud Storage
            if 'cover_image_url' in book_data:
                filename = book_data['cover_image_url'].split('/')[-1]
                blob = bucket.blob(filename)
                blob.delete()

            return 'Book and cover image deleted successfully', 200
        else:
            return 'Book not found', 404
    except Exception as e:
        return str(e), 500
