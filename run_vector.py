from app.text_splitter import TextSplitter
from app.embeddings import Embeddings

file_name = 'faiss_index'
source_file_name = 'basedata.txt'

embeddings = Embeddings(file_name)
splitter = TextSplitter(source_file_name, chunk_size=40, chunk_overlap=15)
docs = splitter.get_split_documents()

print('docs ==>', docs)

# 会在本地目录生成一份faiss_index的文件
embeddings.save_local(docs)
print('success')