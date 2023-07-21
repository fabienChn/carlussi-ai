import os

import constants
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI

def transcript_to_answer(transcript):
    os.environ["OPENAI_API_KEY"] = constants.APIKEY

    query = transcript

    loader = TextLoader('./data.txt')
    index = VectorstoreIndexCreator().from_loaders([loader])

    answer = index.query(query, llm=ChatOpenAI())

    print(answer)

    return answer