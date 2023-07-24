from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def transcript_to_answer(transcript):
    query = transcript

    loader = TextLoader('./data.txt')
    index = VectorstoreIndexCreator().from_loaders([loader])

    answer = index.query(query, llm=ChatOpenAI())

    print(answer)

    return answer