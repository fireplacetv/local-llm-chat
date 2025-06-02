from huggingface_hub import hf_hub_download
import json

with open("model_conf.json", "r") as model_conf_file:
    model_conf = json.load(model_conf_file)
    hf_hub_download(
        repo_id = model_conf["repo_id"],
        filename = model_conf["filename"],
        local_dir = "models",
        local_dir_use_symlinks = False,
    )
