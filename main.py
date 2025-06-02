import json
from llama_cpp import Llama

def load_model(path_to_model):
    """ load the model """

    model = Llama(
        model_path = path_to_model,
        n_gpu_layers = 20,
        n_threads = 8,
        n_ctx = 2048,
        verbose = False
    )

    return model

def chat_loop(model):
    """Run the interactive REPL."""
    print("\n🦙 Local LLM REPL is ready! Type 'exit' to quit.\n")
    GREEN = "\033[92m"
    ORANGE = "\033[38;5;208m"  # True orange using 256-color escape
    RESET = "\033[0m"          # Resets color to default (white)

    prompt_template = "<|user|>\n{user_input}\n<|assistant|>\n"
    chat_history = ""

    while True:
        try:
            user_input = input(f"\n{GREEN}You:{RESET} ").strip()
            if user_input.lower() in {"exit", "quit"}:
                print("👋 Goodbye!")
                break

            full_prompt = chat_history + prompt_template.format(user_input=user_input)

            output = model(
                prompt = full_prompt, 
                max_tokens=1000, 
                stop=["<|user|>", 
                "<|assistant|>"]
            )
            response = output["choices"][0]["text"].strip()

            print(f"\n{ORANGE}ConchAI:{RESET} ", response)
            chat_history += prompt_template.format(user_input=user_input) + response + "\n"

        except KeyboardInterrupt:
            print("\n👋 Interrupted. Goodbye!")
            break

if __name__ == "__main__":
    with open("model_conf.json", "r") as conf_file:
        model_conf = json.load(conf_file)["main"]
        model = load_model("models/" + model_conf["filename"])
        chat_loop(model)
