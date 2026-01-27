# Documentation
## Structure
- **config**: *contain all of info/text based configration*
- **data**: *contain all of dataset*
    - raw_docs
    - chunks
    - vector_store
    - output
- src
    - core: *contain all of based program configuration*
    - domain: *contain all of data domain*
    - services: *contain all of service program*
        - analysis_egnine.py: *contain all steps ritrieval*
        - ingestion_service.py: *contain all steps of preprocessing data (load documents -> chunking -> embedding -> store vector)*
        - pdf_renderer.py
        - rag_service.py: *contain all programs for run the chatbot*
    - utils: *contain all of utils program*
- templates
- test
