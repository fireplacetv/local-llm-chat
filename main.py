import json
import shutil
import textwrap
from llama_cpp import Llama

GREEN = "\033[92m"          # Green color code
YELLOW = "\033[42m\033[30m" # Green background
ORANGE = "\033[38;5;208m"   # True orange using 256-color escape
RESET = "\033[0m"           # Resets color to default (white)

def load_model(model_filename):
    """ load the model """

    path_to_model = "models/" + model_filename
    model = Llama(
        model_path = path_to_model,
        n_gpu_layers = 20,
        n_batch = 1024,
        n_threads = 10,
        n_ctx = 4096,
        low_ram = True,
        verbose = False
    )
    print(f"\nLoading model {YELLOW}" + model_filename + f"{RESET}n")

    return model

def print_response(response):
    """Apply basic wrapping for easier reading on terminal"""
    n_columns = shutil.get_terminal_size().columns
    if n_columns > 80:
        n_columns = 80
    wrapped_response = textwrap.fill(response, width=n_columns).strip()
    print(wrapped_response)

def summarize_chat(chat_history, max_word_length=200):
    """Apply prompt to compress chat history and continue"""
    # don't summarize short chats
    if len(chat_history.split(" ")) < max_word_length:
        return chat_history

    user_input = """
    Review everything we have discussed. 
    Summarize the most important topics in 300 words or fewer.
    """
    prompt_template = "<|user|>\n{user_input}\n<|assistant|>\n"
    full_prompt = chat_history + prompt_template.format(user_input=user_input)
    output = model(
        prompt = full_prompt, 
        max_tokens=1000, 
        stop=["<|user|>", 
        "<|assistant|>"]
    )
    compressed_history = output["choices"][0]["text"]
    return compressed_history

def chat_loop(model):
    """Run the interactive REPL."""
    print("\n🦙 Local LLM is ready! Type 'exit' to quit.")

    prompt_template = "<|user|>\n{user_input}\n<|assistant|>\n"
    chat_history = ""

    while True:
        if len(chat_history.split(" ")) > 2048:
            print("🥡 Compressing Chat History")
            chat_history = summarize_chat(chat_history)

        try:
            user_input = input(f"\n{GREEN}You:{RESET} ").strip()
            if user_input.lower() in {"exit"}:
                print("👋 Goodbye!")
                break
            if user_input.lower() in {"continue"}:
                print("🥡 Compressing Chat History")
                chat_history = summarize_chat(chat_history)
                print("\n New history:\n" + chat_history)
                continue
            if user_input.lower() in {"reset"}:
                chat_history = ""
                print("😱 Chat history erased!")
                continue
            if user_input.lower() in {"history"}:
                print("📜 Chat history:")
                print(chat_history)
                print("Chat stats:")
                print(len(chat_history.split(" ")), "words")
                print(len(chat_history), "characters")
                continue
            if user_input.lower() == "load":
                print("💾 Loading saved chat history")
                file_path = input(f"{ORANGE}Specify file path:{RESET} ").strip()
                with open(file_path, "r") as saved_history:
                    saved_string = str.join(" ",saved_history.readlines())
                    chat_history = str.join(" ", saved_string.split(" ")[:2048])
                print(chat_history)
                continue
            if user_input.lower() == "save":
                print("💾 Saving chat history")
                file_path = input(f"{ORANGE}Specify file path:{RESET} ").strip()
                with open(file_path, "w") as f:
                    f.write(chat_history)
                continue


            print("🧠 Thinking...")

            full_prompt = chat_history + prompt_template.format(user_input=user_input)

            output = model(
                prompt = full_prompt, 
                max_tokens=1000, 
                stop=["<|user|>", 
                "<|assistant|>"]
            )
            response = output["choices"][0]["text"]

            print_response(f"\n{ORANGE}Char Siu BAI:\n{RESET}" + response)
            chat_history += prompt_template.format(user_input=user_input) + response + "\n"

        except KeyboardInterrupt:
            print("\n👋 Interrupted. Goodbye!")
            break

if __name__ == "__main__":
    with open("model_conf.json", "r") as conf_file:
        model_conf = json.load(conf_file)["main"]
        model = load_model(model_conf["filename"])
        chat_loop(model)
