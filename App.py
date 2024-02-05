

import os
os.environ["OPENAI_API_KEY"]="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"
from langchain.vectorstores import FAISS
import streamlit as st
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms.openai import OpenAI
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="BAAI/bge-large-en",
                                                      model_kwargs={"device": "cuda"})


db3 = Chroma(persist_directory="C:/Users/91955/Downloads/New folder (3)/pythonProject6/Model", embedding_function=instructor_embeddings)
qa_chain_instrucEmbed = RetrievalQA.from_chain_type(llm=OpenAI(temperature=0.8),
                                                    chain_type="stuff",
                                                    retriever=db3.as_retriever(),
                                                    return_source_documents=True,
                                                    )


import textwrap

def wrap_text_preserve_newlines(text, width=110):
    # Split the input text into lines based on newline characters
    lines = text.split('\n')

    # Wrap each line individually
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]

    # Join the wrapped lines back together using newline characters
    wrapped_text = '\n'.join(wrapped_lines)

    return wrapped_text

def process_llm_response(llm_response):
    return (wrap_text_preserve_newlines(llm_response['result']))








# # print(llm_response)
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Define a route for your API endpoint
@app.route('/get_answer', methods=['POST'])
def your_endpoint():
    # Get data sent from Node.js
    res = request.json['query'] # Assuming JSON data is sent
    print(res)
    # retriever = db3.as_retriever(search_type="mmr", search_kwargs={'k': 10, 'fetch_k': 50})

    query = f"""Give me Comprehensive answer on Query according Ayurveda:{res}
"""


    llm_response = qa_chain_instrucEmbed(query)
    ans= process_llm_response(llm_response)
    print(ans)

    # Process the data or perform any necessary operations
    # For example, you can access data['query'] if that's what you expect

    # Generate a response
    response_data = {'data':ans}

    # Return the response as JSON
    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)



