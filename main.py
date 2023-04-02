import json
import os
from google.cloud import storage
from flask import Flask, request
from llama_index import GPTSimpleVectorIndex, Document, SimpleDirectoryReader, LLMPredictor, QuestionAnswerPrompt, RefinePrompt
from langchain.chat_models import ChatOpenAI
from openai import ChatCompletion, api_key

app = Flask(__name__)
bucket_name = os.environ.get("BUCKET_NAME", "newbucketismean")


@app.route("/", methods=["POST"])
def hello_world():
    name = os.environ.get("NAME", "World")
    # curl -X POST -H "Content-Type: application/json" -d '{"messages": "What is
    # Supply"}' https://botgptserver-2pzthp6v5a-uc.a.run.app

    messages = request.json["messages"]
    os.environ['OPENAI_API_KEY'] = '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'

    api_key = "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"
    print(messages)
    print("Error may be here")


    # Create a Cloud Storage client object
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Get a blob object representing the file you want to read
    blob = bucket.blob("econTragakes.json")

    print(blob.content_type)
    print(blob.content_encoding)
    # Read the contents of the file
    file_contents = blob.download_as_text(encoding="utf-8")
    # Make sure it's a json string

    # Parse it as a JSON string
    file_contents2 = json.loads(file_contents)
    # Print the index_struct_id
    print(file_contents2["vector_store"]["simple_vector_store_data_dict"]["text_id_to_doc_id"]["63bd4431-d6a7-4926-9267-b79a113947d0"])




    # print the length of the string
    print(len(file_contents))

    # Return the first 100 characters of the string

    # return "Hello {}! Your file contents were: {}".format(name, file_contents)
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"))

    index = GPTSimpleVectorIndex.load_from_string(file_contents)

    response = index.query(messages, llm_predictor=llm_predictor)

    print(response.get_formatted_sources())
    return response.response()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
