import os
import openai
from getpass import getpass
#
import logging
import sys
from pprint import pprint
#
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
#
from llama_index.core import(VectorStoreIndex,
                        SimpleDirectoryReader,
                        load_index_from_storage,
                        StorageContext,
                        ServiceContext,
                        Document)

from llama_index.llms.openai import OpenAI
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core.prompts import PromptTemplate
from llama_index.core.text_splitter import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.postprocessor import MetadataReplacementPostProcessor


documents = SimpleDirectoryReader('./Data/').load_data()
print(len(documents))
pprint(documents)