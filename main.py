import os
from google.cloud import storage

from flask import Flask, request

app = Flask(__name__)
bucket_name = os.environ.get("BUCKET_NAME", "newbucketismean")

@app.route("/", methods=["POST"])
def hello_world():
    name = os.environ.get("NAME", "World")
    
    # Create a Cloud Storage client object
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Get a blob object representing the file you want to read
    blob = bucket.blob("econTragakes.json")

    # Read the contents of the file
    file_contents = blob.download_as_string()

# Return the first 100 characters of the string
    
    # return "Hello {}! Your file contents were: {}".format(name, file_contents)
    return file_contents[:100]

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
