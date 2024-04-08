import urllib3

# Create a PoolManager instance for making requests
http = urllib3.PoolManager()

# The URL of the large file you want to stream
url = "http://images.cocodataset.org/annotations/annotations_trainval2017.zip"

# Open a connection to the URL and request to stream the response
response = http.request('GET', url, preload_content=False)

# Choose a chunk size (number of bytes). This is the size of each part of the file you'll handle at a time.
chunk_size = 1024

# Stream the content, chunk by chunk
with open('annotations/annotations_trainval2017.zip', 'wb') as out:
    while True:
        data = response.read(chunk_size)
        if not data:
            break
        out.write(data)

# Release the connection
response.release_conn()