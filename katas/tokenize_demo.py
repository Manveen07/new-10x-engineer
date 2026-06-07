import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

samples = ["hi", "unhappiness", "Kubernetes", "error code 0x80", "leadlens classifier"]
for text in samples:
    ids = enc.encode(text)
    pieces = [enc.decode([i]) for i in ids]
    print(f"{text!r:25} -> {len(ids)} tokens: {pieces}")
