#!/bin/bash

MODEL="/transfer/huggingface/hub/models--unsloth--Qwen2.5-Coder-7B-Instruct-GGUF/snapshots/0ecf11859560b2bf42e703207f9371186d02245f/Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf"
# MODEL="/transfer/huggingface/hub/models--unsloth--Qwen3-8B-GGUF/snapshots/a6adef130ffb23ddaf1a62fec9dced968c9bc482/Qwen3-8B-UD-Q4_K_XL.gguf"


llama-server \
    --api-key 12345 \
    -c 0 \
    -ngl 999 \
    -m "$MODEL" 

# sleep 5

# echo "Opening browser..."
# xdg-open http://127.0.0.1:8080 
