from huggingface_hub import snapshot_download
model_id="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
snapshot_download(repo_id=model_id, local_dir="input/models/", local_dir_use_symlinks=False, revision="main")