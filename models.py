from pydantic import BaseModel
from enum import Enum

class ModelLocationEnum(str, Enum):
    local = "local"
    huggingface = "huggingface"
    vmwarevllmapi = "vmwarevllmapi"

class InferenceServerEnum(str, Enum):
    Vllm = "Vllm"
    VmwareVllmApi = "VmwareVllmApi"
    NvidiaTriton = "NvidiaTriton"
    LocalFile = "LocalFile"

class IntegratorEnum(str, Enum):
    # Langchain is a framework for developing applications powered by language models
    # You can chain multiple LLMs and other sources of information together
    Langchain = "Langchain" 
    Llamaindex = "Llamaindex"

class ModelEnum(str, Enum):
    Llama = "Llama"
    Mistral = "Mistral"
    Mixtral = "Mixtral"

class ModelPathEnum(str, Enum):
    LlamaLocal = "./models/llama-2-7b-chat.Q4_K_M.gguf"
    MistralLocal = "./models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
    MixtralLocal = "./models/mixtral-8x7b-v0.1.Q4_K_M.gguf"
    LlamaHuggingface = "NousResearch/Llama-2-7b-chat-hf"
    MistralHuggingface = "mistralai/Mistral-7B-Instruct-v0.2"
    MixtralHuggingface = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    LlamaVllm = "meta-llama/Llama-2-13b-chat-hf"
    MistralVllm = "mistralai/Mistral-7B-Instruct-v0.2"
    MixtralVllm = "mistralai/Mixtral-8x7B-Instruct-v0.1"

class TokenizerPathEnum(str, Enum):
    LlamaHuggingface = "NousResearch/Llama-2-7b-chat-hf"

class EmbeddingModelEnum(str, Enum):
    LlamaEmbedding = "sentence-transformers/all-MiniLM-L6-v2"
    # LlamaEmbedding = "BAAI/bge-large-en-v1.5"
    # MistralEmbedding = "sentence-transformers/all-MiniLM-L6-v2"
    MistralEmbedding = "BAAI/bge-large-en-v1.5"
    # MixtralEmbedding = "sentence-transformers/all-MiniLM-L6-v2"
    MixtralEmbedding = "BAAI/bge-large-en-v1.5"


class DeviceEnum(str, Enum):
    CPU = "cpu"
    GPU = "gpu"
    CUDA = "cuda"

class VectorDatabaseEnum(str, Enum):
    FAISS = "faiss"
    Milvus = "milvus"
    Vespa = "vespa"

class ProcessorParams(BaseModel):
    rootPath: str
    modelName: ModelEnum
    device: DeviceEnum
    vectorDatabase: VectorDatabaseEnum
    knowledgeBaseId: str

class Wish(ProcessorParams):
    modelLocation: ModelLocationEnum
    inferenceServer: InferenceServerEnum
    whisper: str

class Information(ProcessorParams):
    folderName: str
    documentName: str
    integrator: IntegratorEnum
