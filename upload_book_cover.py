import functions_framework
from google.cloud import storage, firestore
from werkzeug.utils import secure_filename

storage_client = storage.Client()
firestore_client = firestore.Client()
bucket_name = 'book-cover-image'
bucket = storage_client.bucket(bucket_name)

@functions_framework.http
def upload_book_cover(request):
    try:
        book_id = request.form['id']
        file = request.files['file']
        filename = secure_filename(file.filename) # Sanitize the filename to ensure it's safe
        blob = bucket.blob(filename)
        blob.upload_from_string(file.read(), content_type=file.content_type)
        
        # Construct the public URL of the uploaded file
        url = f"https://storage.googleapis.com/{bucket_name}/{filename}"
        
        # Update Firestore document with the cover image URL
        book_ref = firestore_client.collection('books').document(book_id)
        book_ref.update({'cover_image_url': url})

        return {'url': url}, 200
    except Exception as e:
        return str(e), 500
