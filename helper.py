from models import EmbeddingModelEnum, ModelLocationEnum, ModelEnum, ModelPathEnum, TokenizerPathEnum, Wish

def get_model_path(wish):
    switcher = {
        (ModelLocationEnum.local, ModelEnum.Llama): ModelPathEnum.LlamaLocal,
        (ModelLocationEnum.local, ModelEnum.Mistral): ModelPathEnum.MistralLocal,
        (ModelLocationEnum.huggingface, ModelEnum.Llama): ModelPathEnum.LlamaHuggingface,
        (ModelLocationEnum.huggingface, ModelEnum.Mistral): ModelPathEnum.MistralHuggingface,
        (ModelLocationEnum.vllm, ModelEnum.Llama): ModelPathEnum.LlamaVllm,
        (ModelLocationEnum.vllm, ModelEnum.Mistral): ModelPathEnum.MistralVllm,
    }

    return switcher.get((wish.modelLocation, wish.modelName), None)

def get_embedding_model_path(wish):
    if wish.modelName == ModelEnum.Llama:
        return EmbeddingModelEnum.LlamaEmbedding

def get_tokenizer_path(wish):
    switcher = {
        (ModelLocationEnum.huggingface, ModelEnum.Llama): TokenizerPathEnum.LlamaHuggingface,
    }

    return switcher.get((wish.location, wish.modelName), None)

def get_document_path(wish):
    return f"./data/{wish.documentName}"