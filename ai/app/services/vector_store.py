import pickle
from langchain_community.vectorstores import FAISS
from app.services.embeddings import documents_to_jamodict

def FAISS_vectorize_documents(documents, embedding_model, name):
    try:
        vector_store = FAISS.from_texts(documents, embedding=embedding_model)
        with open(f'{name}.pkl', 'wb') as f:
            pickle.dump(vector_store, f)
        print(f"'{name}.pkl' 파일에 FAISS 벡터 스토어가 성공적으로 저장되었습니다.")
    except Exception as e:
        print(f"FAISS 벡터 스토어 저장 중 오류가 발생했습니다: {e}")
        vector_store = None  # 오류 발생 시 반환할 값을 None으로 설정
    return vector_store

def jamo_vectorize_documents(documents, name):
    try:
        jamodict = documents_to_jamodict(documents)
        with open(f'{name}.pkl', 'wb') as f:
            pickle.dump(jamodict, f)
        print(f"'{name}.pkl' 파일에 자모 딕셔너리가 성공적으로 저장되었습니다.")
    except Exception as e:
        print(f"자모 딕셔너리 저장 중 오류가 발생했습니다: {e}")
        jamodict = None  # 오류 발생 시 반환할 값을 None으로 설정

    return jamodict