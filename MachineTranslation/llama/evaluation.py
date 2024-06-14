import os
import sys
import json
from tqdm import tqdm
import sacrebleu
import fire
import gradio as gr
import torch
import transformers
from peft import PeftModel
from transformers import GenerationConfig, LlamaForCausalLM, LlamaTokenizer

from utils.callbacks import Iteratorize, Stream
from utils.prompter import Prompter
from utilss import ListWriter
if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

try:
    if torch.backends.mps.is_available():
        device = "mps"
except:  # noqa: E722
    pass


def load_json(json_file):
    with open(json_file) as f:
        data = json.load(f)
    return data


def save_to_file(data, file):
    with open(file, "w") as f:
        for item in data:
            f.write("%s\n" % item)

def main(
    load_8bit: bool = False,
    base_model: str = "",
    lora_weights: str = "",
    prompt_template: str = "",
    server_name: str = "0.0.0.0",
    share_gradio: bool = False,
    json_file: str = "/PATH_TO/general-pidgin-modeling/llama/data/eval_dataset.json.json",
    pcm_preds_output_file: str = "pcm_preds_output.txt",
    en_preds_output_file: str = "en_preds_output.txt",
    results_output_file: str = "results_output_file"
):
    base_model = base_model or os.environ.get("BASE_MODEL", "")
    assert (
        base_model
    ), "Please specify a --base_model, e.g. --base_model='huggyllama/llama-7b'"

    prompter = Prompter(prompt_template)
    tokenizer = LlamaTokenizer.from_pretrained(base_model)

    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"

    if device == "cuda":
        model = LlamaForCausalLM.from_pretrained(
            base_model,
            load_in_8bit=load_8bit,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        model = PeftModel.from_pretrained(
            model,
            lora_weights,
            torch_dtype=torch.float16,
        )
    elif device == "mps":
        model = LlamaForCausalLM.from_pretrained(
            base_model,
            device_map={"": device},
            torch_dtype=torch.float16,
        )
        model = PeftModel.from_pretrained(
            model,
            lora_weights,
            device_map={"": device},
            torch_dtype=torch.float16,
        )
    else:
        model = LlamaForCausalLM.from_pretrained(
            base_model, device_map={"": device}, low_cpu_mem_usage=True
        )
        model = PeftModel.from_pretrained(
            model,
            lora_weights,
            device_map={"": device},
        )

    model.config.pad_token_id = tokenizer.pad_token_id = 0  # unk
    model.config.bos_token_id = 1
    model.config.eos_token_id = 2

    if not load_8bit:
        model.half()

    model.eval()
    if torch.__version__ >= "2" and sys.platform != "win32":
        model = torch.compile(model)

    def evaluate(
        instruction,
        input=None,
        temperature=0.1,
        top_p=0.75,
        top_k=40,
        num_beams=4,
        max_new_tokens=128,
        stream_output=False,
        **kwargs,
    ):
        prompt = prompter.generate_prompt(instruction, input)
        inputs = tokenizer(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"].to(device)
        generation_config = GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            num_beams=num_beams,
            **kwargs,
        )

        generate_params = {
            "input_ids": input_ids,
            "generation_config": generation_config,
            "return_dict_in_generate": True,
            "output_scores": True,
            "max_new_tokens": max_new_tokens,
        }

        with torch.no_grad():
            generation_output = model.generate(
                input_ids=input_ids,
                generation_config=generation_config,
                return_dict_in_generate=True,
                output_scores=True,
                max_new_tokens=max_new_tokens,
            )
        s = generation_output.sequences[0]
        output = tokenizer.decode(s)
        yield prompter.get_response(output)

    data = load_json(json_file)
    predict_english_results = []
    predict_pcm_results = []
    english_prediction = []
    pcm_prediction = []
    pcm_truth = []
    english_truth = []
    results = []
    
    for item in tqdm(data, desc="Processing the evaluation data", unit="item"):
        instruction = item["instruction"]
        input_text = item["input"]
        true_translation_text = item["output"]
        output = next(evaluate(instruction, input_text))
        if instruction == "translate English to Nigerian Pidgin" :
            # print("translate English to Nigerian Pidgin")
            pcm_truth.append(true_translation_text)
            predict_pcm_results.append(
                f"Instruction: {instruction}  \nInput: {input_text} \nOutput: {output}"
            )
            pcm_prediction.append(output)
        else:
            # print("translate Nigerian Pidgin to English")
            english_truth.append(true_translation_text)
            predict_english_results.append(
                f"Instruction: {instruction} \nInput: {input_text} \nOutput: {output}"
            )
            english_prediction.append(output)
    
    save_to_file(predict_english_results, en_preds_output_file)
    save_to_file(predict_pcm_results, pcm_preds_output_file)
    ListWriter("/PATH_TO/general-pidgin-modeling/llama/evaluationChecker/lists/preds/pcm.txt", pcm_prediction)
    ListWriter("/PATH_TO/general-pidgin-modeling/llama/evaluationChecker/lists/preds/en.txt", english_prediction)
    ListWriter("/PATH_TO/general-pidgin-modeling/llama/evaluationChecker/lists/real/pcm.txt", pcm_truth)
    ListWriter("/PATH_TO/general-pidgin-modeling/llama/evaluationChecker/lists/real/en.txt", english_truth)
    print(f"the length of PCM predictions is {len(pcm_prediction)} and pcm truth {len(pcm_truth)}")
    print(f"the BLUE score for enlgish to pcm trasnlation {sacrebleu.corpus_bleu(pcm_prediction, pcm_truth).score}") 
    print(f"the BLUE score for pcm to english trasnlation {sacrebleu.corpus_bleu(english_prediction, english_truth).score}")        
   
if __name__ == "__main__":
    fire.Fire(main)
