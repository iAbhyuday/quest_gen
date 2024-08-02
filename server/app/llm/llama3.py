import os
from langchain_community.llms import LlamaCpp



n_gpu_layers = int(os.environ.get('N_GPU_LAYERS'))
n_ctx = int(os.environ.get('N_CTX'))
temperature = float(os.environ.get('TEMP'))

n_batch = 512  


model = os.environ.get('MODEL_NAME')


# Make sure the model path is correct for your system!
llm = LlamaCpp(
    model_path=f"/models/{model}",
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    f16_kv=True,
    n_ctx=n_ctx,
    verbose=True, 
    temperature=temperature,
    stop=["<|eot_id|>"],
    echo=True,
    max_tokens=2000,
    streaming=True
)
