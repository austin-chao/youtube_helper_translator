from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.blob_loaders.youtube_audio import (
    YoutubeAudioLoader,
)
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import (
    OpenAIWhisperParser,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv, dotenv_values

load_dotenv()

embeddings = OpenAIEmbeddings()

# set a flag to switch between local and remote parsing
# change this to True if you want to use local parsing
local = False

def create_vector_db_from_youtube_url(video_url: str) -> FAISS:
    loader = YoutubeLoader.from_youtube_url(video_url,add_video_info=False)
    transcript = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
    docs = text_splitter.split_documents(transcript)

    db = FAISS.from_documents(docs,embeddings)
    return db
    
def create_vector_db_from_youtube_audio(video_url: str) -> FAISS:
    # Directory to save audio files
    save_dir = "./youtube_videos"
    video_urls = [video_url]

    # Transcribe the videos to text
    if local:
        loader = GenericLoader(
            YoutubeAudioLoader(video_urls, save_dir), OpenAIWhisperParserLocal()
        )
    else:
        loader = GenericLoader(YoutubeAudioLoader(video_urls, save_dir), OpenAIWhisperParser())
    transcript = loader.load()
    
    #split the text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
    docs = text_splitter.split_documents(transcript)

    db = FAISS.from_documents(docs,embeddings)
    return db
    
def get_response_from_query(db,query,k=4):

    docs = db.similarity_search(query,k=k)
    docs_page_content = " ".join([d.page_content for d in docs])

    llm = OpenAI(model="gpt-3.5-turbo-instruct")

    prompt = PromptTemplate(
        input_variables=["question","docs"],
        template = """
        You are a helpful assistant that that can answer questions about youtube videos 
        based on the video's transcript.
        
        Answer the following question: {question}
        By searching the following video transcript: {docs}
        
        Only use the factual information from the transcript to answer the question.
        
        If you feel like you don't have enough information to answer the question, say "I don't know".
        
        Your answers should be verbose and detailed.
        """
    )

    chain=LLMChain(llm=llm,prompt=prompt)

    response = chain.run(question=query,docs=docs_page_content)
    response = response.replace("\n","")

    return response

def clear_vector_db(db):
    #check if index exists
    db.index.reset()
    pass