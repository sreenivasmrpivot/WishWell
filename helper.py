from models import EmbeddingModelEnum, ModelLocationEnum, ModelEnum, ModelPathEnum, TokenizerPathEnum, Wish

def get_model_path(wish):
    switcher = {
        (ModelLocationEnum.local, ModelEnum.Llama): ModelPathEnum.LlamaLocal,
        (ModelLocationEnum.local, ModelEnum.Mistral): ModelPathEnum.MistralLocal,
        (ModelLocationEnum.local, ModelEnum.Mixtral): ModelPathEnum.MixtralLocal,
        (ModelLocationEnum.huggingface, ModelEnum.Llama): ModelPathEnum.LlamaHuggingface,
        (ModelLocationEnum.huggingface, ModelEnum.Mistral): ModelPathEnum.MistralHuggingface,
        (ModelLocationEnum.huggingface, ModelEnum.Mixtral): ModelPathEnum.MixtralHuggingface,
        (ModelLocationEnum.vmwarevllmapi, ModelEnum.Llama): ModelPathEnum.LlamaVllm,
        (ModelLocationEnum.vmwarevllmapi, ModelEnum.Mistral): ModelPathEnum.MistralVllm,
        (ModelLocationEnum.vmwarevllmapi, ModelEnum.Mixtral): ModelPathEnum.MixtralVllm,
    }

    return switcher.get((wish.modelLocation, wish.modelName), None)

def get_embedding_model_path(wish):
    if wish.modelName == ModelEnum.Llama:
        return EmbeddingModelEnum.LlamaEmbedding
    elif wish.modelName == ModelEnum.Mistral:
        return EmbeddingModelEnum.MistralEmbedding
    elif wish.modelName == ModelEnum.Mixtral:
        return EmbeddingModelEnum.MixtralEmbedding

def get_tokenizer_path(wish):
    switcher = {
        (ModelLocationEnum.huggingface, ModelEnum.Llama): TokenizerPathEnum.LlamaHuggingface,
    }

    return switcher.get((wish.modelLocation, wish.modelName), None)

def get_document_path(wish):
    return f"./data/{wish.documentName}"