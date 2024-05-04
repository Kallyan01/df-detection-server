import hashlib

def hash_url(url):
    # Convert the URL string to bytes
    url_bytes = url.encode('utf-8')

    # Hash the URL using SHA-256
    hash_object = hashlib.sha256()
    hash_object.update(url_bytes)
    hashed_url = hash_object.hexdigest()

    return hashed_url