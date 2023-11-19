# CPU run
# python3 wish_processor.py --device cpu --modelLocation local --documentName "BCOM 2024 benefits.pdf" --modelName Llama --channel Langchain --vectorDatabase faiss --whisper "What is the coverage for Orthodontia with Broadcom?"

# GPU run
# python3 wish_processor.py --device cuda --modelLocation local --documentName "BCOM 2024 benefits.pdf" --modelName Llama --channel Langchain --vectorDatabase milvus --whisper "What is the coverage for Orthodontia with Broadcom?" --debug True