from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List


class TextSplitter():

    def __init__(self, path: str, chunk_size: int = 20, chunk_overlap: int = 8, separators: List = ["\n\n"]) -> None:
        print('TextSplitter => START')

        self.path = path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators
        pass

    def get_split_documents(self):

        if not self.path:
            raise ValueError('path is empty')
        else:
            loader = TextLoader(self.path, encoding="utf-8")
            documents = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap, separators=self.separators)

            return splitter.split_documents(documents)