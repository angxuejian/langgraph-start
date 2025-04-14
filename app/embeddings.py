from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


class Embeddings():

    def __init__(self, file_name: str = 'faiss_index') -> None:
        print('Embeddings => START')

        self.file_name = file_name
        self.hf = None
        self._init_hf()
        pass

    def _init_hf(self):
        print('HuggingFaceEmbeddings loading....')
        model_name = "BAAI/bge-base-zh"
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': False }
        hf = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )

        self.hf = hf
        print('HuggingFaceEmbeddings done !')

    def save_local(self, docs):
        vector_store = FAISS.from_documents(docs, self.hf)
        vector_store.save_local(self.file_name)

    def query(self, text: str, k: int = 1):
        db = FAISS.load_local(self.file_name, self.hf, allow_dangerous_deserialization=True)

        results = db.similarity_search(text, k=k)

        return results