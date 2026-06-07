# Fundamentals — recall cheat-sheet

How LLMs work under the hood. For interview "explain X" questions + the foundation of RAG/agents months. Revise this every session start until all 🟢.

---

## Token

- Smallest unit the model works in. Text → tokens → integer IDs. Model predicts the next ID, repeatedly. "An LLM is a next-token predictor; everything else is consequence."
- **Subwords**, not whole words or single chars. "unhappiness" → "un" + "happiness". "hi" → 1 token.
- Built by **BPE (Byte-Pair Encoding)**: frequent character pairs get merged into one token. Common sequences = 1 token (cheap); rare = split.
- Why subwords: words → vocab too huge + can't handle new words; chars → sequences too long. Subwords balance.
- Rule of thumb: **~4 chars ≈ 1 token** (English). 100 tokens ≈ 75 words.
- Status: 🟢 (got BPE intuition without the name)
- **Saw it (tiktoken cl100k_base):** `hi`→1 tok; `unhappiness`→`['un','h','appiness']`; `Kubernetes`→`['K','ubernetes']`; `error code 0x80`→`['error',' code',' ','0','x','80']`; `leadlens`→`['lead','l','ens']`.
- **The 0x80 lesson (token → RAG chain):** exact codes shatter into generic meaningless tokens (`0`,`x`,`80`) → no clean embedding → dense/vector search can't find them → BM25 (literal string match) can → **this is WHY hybrid (dense+BM25) beats pure dense.** ~35% of real queries carry exact identifiers that shatter this way. Saw the mechanism, didn't just read the claim.

## Embedding

- A **vector (list of numbers) representing meaning** in high-dimensional space. Similar meaning → nearby vectors ("king"≈"queen", far from "banana").
- NOT the same as weights/biases (those are model *parameters*). The token-embedding table IS a learned weight matrix (lookup: token ID → vector), but the *concept* "embedding" = the meaning-vector, not all params.
- **Why it's load-bearing:** vector search / RAG = embed query + embed chunks → return chunks whose vector is nearest. "Search" becomes "find nearest vectors."
- **Similarity = cosine, not raw dot product.** Cosine = dot product of *normalized* vectors → measures direction only, ignores magnitude. Raw dot product is skewed by vector length. Direction carries meaning, not magnitude.
- **Ties to RAG month:** vector search finds paraphrases ("K8s"≈"Kubernetes") but misses exact codes ("error 0x80" has no semantic neighbor) → why hybrid (BM25 + dense) is needed.
- "Embeddings turn meaning into geometry — similar things sit close."
- Status: 🟢 (corrected: embedding = meaning-vector, NOT weights/biases. Similarity = cosine.)

## Attention

- Every token looks at all other tokens and decides how much each matters for understanding it.
- **Q/K/V:** each token emits Query ("what am I looking for"), Key ("what I offer"), Value ("what I pass on").
- Token A (being updated) uses **its Query** against **every other token's Key**. A asks, B offers. score = A_query · B_key.
- **Full pipeline (order matters):** Q·K → **÷ √d_k** (scaled dot-product; prevents giant scores breaking softmax gradients) → **mask future = −∞** (causal/decoder LMs only — GPT/Gemini; encoders/BERT see both ways) → **softmax** (exp → ÷ sum → normalize to 0–1, weights sum to 1) → **weighted sum of Values**.
- Output = token's new representation = blend of all tokens' Values, weighted by relevance.
- Example: "the animal didn't cross the street because **it** was tired" — "it" attends to "animal" (high) not "street" (low).
- **Multi-head** = many heads in parallel, each learns a different relation (grammar, reference, …), outputs concatenated.
- THE transformer mechanism ("Attention Is All You Need" = stacked attention).
- "Attention = every token asking every other 'how relevant are you?' via query·key, scale by √d_k, mask the future, softmax, blend values."
- **d_k = dimension of key/query vectors** (e.g. 64 → √d_k = 8).
- **Why ÷√d_k:** dot product = sum of d_k products → its variance ≈ d_k → big d_k makes scores large+spread → softmax goes "peaky" (one ≈1, rest ≈0) → gradient ≈ 0 → training stalls. Dividing by √d_k pulls variance back to ~1, keeps softmax smooth, gradients flowing. "Scores scale with key dim, so big d_k saturates softmax and kills gradients; √d_k normalizes it."
- **Causal mask = ADD (not multiply):** matrix with 0 on lower triangle + diagonal, −∞ on upper. Add to scaled scores → future positions become −∞ → softmax → 0. (Add-of-−∞ is canonical; multiply-by-1s also exists.)
- Status: 🟢 (full pipeline incl. why-√d_k + add-mask nuance.)

---

## Re-test queue (ask these next session, no notes)
1. Attention full pipeline incl. the √d_k step + why it exists (the step you half-knew)
2. Cosine vs raw dot product — why cosine for RAG?
3. Causal mask — what is it, which model types use it?
All three of token/embedding/attention reached 🟢 this session. Re-test in 2 days to confirm retention, not comprehension.

## Still to cover (weekday drips)
transformer stack · temperature/sampling · context window + KV cache cost · prompt patterns · function calling · ML basics vocab (supervised/unsupervised/overfitting)
