from pydantic import BaseModel
from enum import Enum

class ModelLocationEnum(str, Enum):
    local = "local"
    huggingface = "huggingface"
    vmwarevllmapi = "vmwarevllmapi"

class ChannelEnum(str, Enum):
    # Langchain is a framework for developing applications powered by language models
    # You can chain multiple LLMs and other sources of information together
    Langchain = "Langchain" 
    Llamaindex = "Llamaindex"
    Vllm = "Vllm"
    VmwareVllmApi = "VmwareVllmApi"

class ModelEnum(str, Enum):
    Llama = "Llama"
    Mistral = "Mistral"

class ModelPathEnum(str, Enum):
    LlamaLocal = "./models/llama-2-7b-chat.Q4_K_M.gguf"
    MistralLocal = "TheBloke/Mistral-7B-Instruct-v0.1-GGUF"
    LlamaHuggingface = "NousResearch/Llama-2-7b-chat-hf"
    MistralHuggingface = "NousResearch/Mistral-1000m-hf" # update this
    LlamaVllm = "meta-llama/Llama-2-13b-chat-hf"
    MistralVllm = "mistralai/Mistral-7B-Instruct-v0.1"

class TokenizerPathEnum(str, Enum):
    LlamaHuggingface = "NousResearch/Llama-2-7b-chat-hf"

class EmbeddingModelEnum(str, Enum):
    LlamaEmbedding = "sentence-transformers/all-MiniLM-L6-v2"

class DeviceEnum(str, Enum):
    CPU = "cpu"
    GPU = "gpu"
    CUDA = "cuda"

class VectorDatabaseEnum(str, Enum):
    FAISS = "faiss"
    Milvus = "milvus"

class Wish(BaseModel):
    rootPath: str
    device: DeviceEnum
    modelLocation: ModelLocationEnum
    documentName: str
    modelName: ModelEnum
    channel: ChannelEnum
    vectorDatabase: VectorDatabaseEnum
    whisper: str