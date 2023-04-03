import json
import os
from google.cloud import storage
from flask import Flask, request
from llama_index import GPTSimpleVectorIndex, Document, SimpleDirectoryReader, LLMPredictor, QuestionAnswerPrompt, RefinePrompt, PromptHelper
from langchain.chat_models import ChatOpenAI
from openai import ChatCompletion, api_key


app = Flask(__name__)
bucket_name = os.environ.get("BUCKET_NAME", "newbucketismean")
# CORS(app)
# INitialize CORS 

def set_cors_headers(response):
    response.headers.set("Access-Control-Allow-Origin", "*")
    response.headers.set("Access-Control-Allow-Headers", "Content-Type")
    response.headers.set("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response


@app.route("/", methods=["POST", "OPTIONS"])
def hello_world():
    if request.method == "OPTIONS":
        # Handle the preflight request and return an empty response with CORS headers
        response = app.make_default_options_response()
        set_cors_headers(response)
        return response

    # The rest of your original code

    name = os.environ.get("NAME", "World")
    # curl -X POST -H "Content-Type: application/json" -d '{"messages": "What is
    # Supply"}' https://botgptserver-2pzthp6v5a-uc.a.run.app

    messages = request.json["messages"]
    book = request.json["book"]
    os.environ['OPENAI_API_KEY'] = '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'
    email = request.json["email"]
    # Create a Cloud Storage client object
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Get a blob object representing the file you want to read
    blob = bucket.blob(book)
    print(messages)
    print(email)
    # Read the contents of the file
    file_contents = blob.download_as_text(encoding="utf-8")
    # Make sure it's a json string

    # return "Hello {}! Your file contents were: {}".format(name, file_contents)
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"))

    max_input_size = 2000
    num_output = 256
    # chunk_size_limit = 1000 # token window size per document
    # embedding_limit = 1000 # max number of embeddings to use per document
    max_chunk_overlap = 20 # overlap for each token fragment
    prompt_helper = PromptHelper(max_input_size=max_input_size, num_output=num_output, max_chunk_overlap=max_chunk_overlap )
    index = GPTSimpleVectorIndex.load_from_string(file_contents, prompt_helper=prompt_helper, llm_predictor=llm_predictor)

    response = index.query(messages, llm_predictor=llm_predictor)
    
    flask_response = app.response_class(
        response=json.dumps(response.response),
        status=200,
        mimetype='application/json'
    )
    set_cors_headers(flask_response)
    return flask_response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
