import os
from src.logger import logger
import torch
from FlagEmbedding import BGEM3FlagModel

LOCAL_MODEL_PATH = "./models/bge-m3"

MODEL_PATH = "BAAI/bge-m3"
if os.path.exists(LOCAL_MODEL_PATH):
    MODEL_PATH = LOCAL_MODEL_PATH
    logger.info(f"Using local model path: {MODEL_PATH}")
else:
    logger.info(f"Using remote model path: {MODEL_PATH}")

is_cuda = torch.cuda.is_available()
device = "cuda" if is_cuda else "cpu"

embedding_model = BGEM3FlagModel(
    MODEL_PATH,
    device=device,
    use_fp16=is_cuda,
)

logger.info("Model loaded on", device)

DENSE_DIM = embedding_model.model.model.config.hidden_size #1024
VOCAB_SIZE = embedding_model.tokenizer.vocab_size #250002