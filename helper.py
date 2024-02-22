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

def get_embedding_model_path(modelName):
    if modelName == ModelEnum.Llama:
        return EmbeddingModelEnum.LlamaEmbedding
    elif modelName == ModelEnum.Mistral:
        return EmbeddingModelEnum.MistralEmbedding
    elif modelName == ModelEnum.Mixtral:
        return EmbeddingModelEnum.MixtralEmbedding

def get_tokenizer_path(wish):
    switcher = {
        (ModelLocationEnum.huggingface, ModelEnum.Llama): TokenizerPathEnum.LlamaHuggingface,
    }

    return switcher.get((wish.modelLocation, wish.modelName), None)

def get_document_path(processorParams):
    return f"./data/{processorParams.folderName}"