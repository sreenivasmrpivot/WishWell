# Demo Script

### Scenario 1: LLM is still relevant - Generic query using vllm [UI](https://vllm.libra.decc.vmware.com/) --> use Llama 13b. 

``` zsh
What is the currency of Qatar?
```

### Scenario 2: LLM is out of relevance - Generic query using vllm [UI](https://vllm.libra.decc.vmware.com/) --> use Llama 13b.

``` zsh
Which is the most populus country?
```

### Scenario 3: LLM is hallucinating - Domain specific query using vllm [UI](https://vllm.libra.decc.vmware.com/) --> use Llama 13b.

``` zsh
What is the coverage for Orthodontia with Broadcom?
```

### Scenario 4: LLM is out of relevance - Generic query using vllm [UI](https://vllm.libra.decc.vmware.com/) --> use Mistral a different LLM.

``` zsh
Which is the most populus country?
```

*** 
    Note: 
        Talk about Mistral size and context length. 
***

### Scenario 5: Generic query using vllm API --> use Llama 7b.

``` zsh
curl -X 'POST'   'http://127.0.0.1:3003/wish/'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "device": "cpu",
  "modelLocation": "vmwarevllmapi",
  "documentName": "BCOM 2024 benefits.pdf",
  "modelName": "Llama",
  "channel": "VmwareVllmApi",
  "whisper": "What is the currency of Qatar?"
}'
```

### Scenario 6: Domain specific query using vllm API (hallucination).

``` zsh
curl -X 'POST'   'http://127.0.0.1:3003/wish/'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "device": "cpu",
  "modelLocation": "vmwarevllmapi",
  "documentName": "BCOM 2024 benefits.pdf",
  "modelName": "Llama",
  "channel": "VmwareVllmApi",
  "whisper": "What is the coverage for Orthodontia with Broadcom?"
}'
```

*** 
    Note: 
        Provide a code walk through for Vllm API. 
***

### Scenario 7: Domain specific query using Langchain RAG. (Model Location changed)

``` zsh
curl -X 'POST'   'http://127.0.0.1:3003/wish/'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "device": "cpu",
  "modelLocation": "local",
  "documentName": "BCOM 2024 benefits.pdf",
  "modelName": "Llama",
  "channel": "Langchain",
  "whisper": "What is the coverage for Orthodontia with Broadcom?"
}'
```

*** 
    Note: 
        Talk about quantization.
        Provide a code walk through for Langchain RAG. 
***

### Scenario 8: Domain specific query using Llamaindex RAG. (Model Location changed)

``` zsh
curl -X 'POST'   'http://127.0.0.1:3003/wish/'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "device": "cpu",
  "modelLocation": "local",
  "documentName": "BCOM 2024 benefits.pdf",
  "modelName": "Llama",
  "channel": "Llamaindex",
  "whisper": "What is the coverage for Orthodontia with Broadcom?"
}'
```

*** 
    Note: 
        Provide a code walk through for Llamaindex RAG. 
***
