# Local-LLM-Chat

Basic command line chat program to experiment with LLMs.

## Set Up

### `models/` folder & `model_conf.json`
To set up, create a json file in the root folder, `model_conf.json` and a
subfolder called `models`:

```
local-llm-chat/
  models/
  model_conf.json
```

In `model_conf.json` specify an object `download_model` with 
`repo_id` and `filename` from HuggingFace, eg:
```
{
	"download_model": {
		"repo_id": "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
		"filename": "tinyllama-1.1b-chat-v1.0.Q2_K.gguf"
	}
}
```

### `download_model.py`
Then use `uv` to run the `download_model.py` script to download the model 
to `models/`:
```
uv run download_model.py
```

## Running

### Choose a model

In `model_conf.json` add an object called `main` with a `filename` (you
don't have to specify the `models/` folder since that's hard coded):

```
{
	"download_model": { ... }
	"main": {
		"filename": "tinyllama-1.1b-chat-v1.0.Q2_K.gguf"
	}
}
```

Use `uv` to run `main.py`:

```
uv run main.py
```

You can type `exit` at any point to quit.



