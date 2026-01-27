import os
import shutil
from typing import List

from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter # untuk memecah text
from langchain_community.document_loaders import PyPDFLoader # untuk baca file
from langchain_chroma import Chroma # untuk database vector

from src.core.config import settings # akses konfigurasi sistem
from src.core.logger import get_logger # akses sistem logging

class IngestionService():
    def __init__(self):
        self.logger = get_logger("IngestionService")

        self.pdf_dir = settings.DATA_DIR / "raw_docs"
        self.db_dir = settings.CHROMA_PERSIST_DIR

        self.chunk_size = 1000
        self.chunk_overlap = 200
    
    def load_pdfs(self) -> List[Document]:
        """
        Docstring for load_pdfs
            1. Cek apakah folder PDF ada? Jika tidak, log error dan return list kosong.
            2. Looping semua file di folder tersebut yang berakhiran .pdf.
            3. Gunakan PyPDFLoader untuk memuat setiap file.
            4. Gabungkan semua hasil load (docs) ke dalam satu list besar.
            5. Return list dokumen tersebut.
        Hint: Gunakan os.listdir atau pathlib.Path.glob.
        """
        documents = []

        if not os.path.exists(self.pdf_dir):
            self.logger.info("File/Folder not Exist")
            return []
        
        files = [f for f in os.listdir(self.pdf_dir) if f.endswith(".pdf")]
        self.logger.info(f"Ditemukan {len(files)} file PDF.")

        for file_name in files:
            file_path = self.pdf_dir/file_name
            try:
                loader = PyPDFLoader(str(file_path))
                docs = loader.load()
                documents.extend(docs)
                self.logger.info(f"Loaded: {file_name} ({len(docs)} pages)")
            except Exception as e:
                self.logger.error(f"Failed to load {file_name}: {str(e)}")
        return documents
        
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Docstring for split_documents
        Logic:
            1. Inisialisasi RecursiveCharacterTextSplitter.
            2. Set chunk_size=1000 (agar konteks cukup luas).
            3. Set chunk_overlap=200 (agar kalimat di perbatasan tidak terpotong maknanya).
            4. Jalankan fungsi split pada input documents.
            5. Return hasil split (chunks).
        """
        if not documents:
            self.logger.info("The documents for splitted is empty")
            return []

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=False)
        
        chunks = text_splitter.split_documents(documents)
        self.logger.info(f"Split {len(documents)} docs into {len(chunks)} chunks.")
        # self.logger.info(f"type of variable chunks is: {type(chunks)}")
        try:
            chunks_dir = os.path.join(settings.DATA_DIR,"chunks")
            if os.path.exists(chunks_dir):
                try:
                    shutil.rmtree(chunks_dir)
                    self.logger.info("The old chunks has been successfully deleted (Reset).")
                except Exception as e:
                    self.logger.error(f"Failed to delete the old DB: {str(e)}")
            
            if not os.path.exists(chunks_dir):
                os.makedirs(chunks_dir)

            chunks_path = os.path.join(chunks_dir, "chunks.txt")


            with open(chunks_path, 'w') as file:
                for item in chunks:
                    file.write(f"{item}\\n")
            self.logger.info(f"Successfully store chunks in {chunks_path}")
        except Exception as e:
            self.logger.info(f"Failed to store chunks: {str(e)}")

        return chunks
    
    def save_to_chroma(self, chunks: List[Document]):
        """
        1. Clean Up: Hapus folder DB lama jika ada (shutil.rmtree).
        2. Instansiasi Embedding Model: Gunakan class GoogleGenerativeAIEmbeddings. Parameternya:
            a. model: Ambil dari settings.EMBEDDING_MODEL (Isinya: models/text-embedding-004).
            b. google_api_key: Ambil dari settings.GOOGLE_API_KEY.
            c. task_type: Isi dengan string "retrieval_document".
                i. Kenapa? Sesuai dokumentasi Google: "Embeddings optimized for document search."
        3. Simpan ke Chroma: Panggil Chroma.from_documents(...).
            a. documents: chunks.
            b. embedding: object embedding google tadi.
            c. persist_directory: path dari settings.
        """

        if not chunks:
            self.logger.warning("Chunks is empty.")
            return
        
        if self.db_dir.exists():
            try:
                shutil.rmtree(self.db_dir)
                self.logger.info("The old database has been successfully deleted (Reset).")
            except Exception as e:
                self.logger.error(f"Failed to delete the old DB: {str(e)}")
        
        try:
            embeddings = GoogleGenerativeAIEmbeddings(
                model=settings.EMBEDDING_MODEL,
                task_type="retrieval_document",
                google_api_key=settings.GOOGLE_API_KEY)

            Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                persist_directory=str(self.db_dir)
            )
            self.logger.info(f"Successfully saved {len(chunks)} vector to {str(self.db_dir)}")
        except Exception as e:
            self.logger.error(f"Failed saved vector: {e}")


    def run(self):
        self.logger.info("=== START INGESTION ===")
        
        raw_docs = self.load_pdfs()

        if raw_docs:
            chunks=self.split_documents(raw_docs)
            self.save_to_chroma(chunks)
        else:
            self.logger.warning("Ingestion cancelled due to lack of documents")

        self.logger.info("=== FINISH INGESTION ===")

