from FlagEmbedding import BGEM3FlagModel

embedding_model = BGEM3FlagModel(
    'BAAI/bge-m3',
    use_fp16=True,
    device='cuda'
)

DENSE_DIM = embedding_model.model.model.config.hidden_size #1024
VOCAB_SIZE = embedding_model.tokenizer.vocab_size #250002