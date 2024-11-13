from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def parse_codebase(path):
    loader = DirectoryLoader(path, glob="**/*.py")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = splitter.split_documents(documents)

    project_details = {
        "project_name": path.split('/')[-1],
        "files": [doc.metadata["source"] for doc in documents],
        "key_functions": [doc.page_content[:200] for doc in split_docs[:5]]
    }

    return project_details
