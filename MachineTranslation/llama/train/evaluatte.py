import os
import sys
import json
import fire
import sacrebleu
import gradio as gr
import torch
import transformers
from peft import PeftModel
from transformers import GenerationConfig, LlamaForCausalLM, LlamaTokenizer
import tqdm
from utils.callbacks import Iteratorize, Stream
from utils.prompter import Prompter


def load_json(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def write_txt(path, content):
    with open(path, 'w') as f:
        f.write(content)

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

try:
    if torch.backends.mps.is_available():
        device = "mps"
except:
    pass

def main(load_8bit: bool = False, base_model: str = "", lora_weights: str = "tloen/alpaca-lora-7b", prompt_template: str = ""):
    base_model = base_model or os.environ.get("BASE_MODEL", "")
    assert base_model, "Please specify a --base_model, e.g. --base_model='huggyllama/llama-7b'"
    prompter = Prompter(prompt_template)
    tokenizer = LlamaTokenizer.from_pretrained(base_model)



    if device == "cuda":
        model = LlamaForCausalLM.from_pretrained(base_model, load_in_8bit=load_8bit, torch_dtype=torch.float16, device_map="auto")
        model = PeftModel.from_pretrained(model, lora_weights, torch_dtype=torch.float16)
    elif device == "mps":
        model = LlamaForCausalLM.from_pretrained(base_model, device_map={"": device}, torch_dtype=torch.float16)
        model = PeftModel.from_pretrained(model, lora_weights, device_map={"": device}, torch_dtype=torch.float16)
    else:
        model = LlamaForCausalLM.from_pretrained(base_model, device_map={"": device}, low_cpu_mem_usage=True)
        model = PeftModel.from_pretrained(model, lora_weights, device_map={"": device})

    model.config.pad_token_id = tokenizer.pad_token_id = 0
    model.config.bos_token_id = 1
    model.config.eos_token_id = 2
    # model.half()
    instruction_marker = '### Instruction:'

    if not load_8bit:
        model.half()  # seems to fix bugs for some users.
    model.eval()
    if torch.__version__ >= "2" and sys.platform != "win32":
        model = torch.compile(model)

    def evaluate(instruction, input=None, temperature=0.1, top_p=0.75, top_k=40, num_beams=4, max_new_tokens=128,
             stream_output=False, **kwargs):
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
        modelResponse = prompter.get_response(output)
        instruction_position = modelResponse.find(instruction_marker)
        data_before_instruction = modelResponse[:instruction_position]

        # Remove duplicates from data_before_instruction
        unique_lines = []
        for line in data_before_instruction.split('\n'):
            line = line.strip()
            if line not in unique_lines:
                unique_lines.append(line)
        print(unique_lines[0])
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!11")
        print(modelResponse)
        return modelResponse, unique_lines[0]



    # if device == "cuda":
    #     model = LlamaForCausalLM.from_pretrained(base_model, load_in_8bit=load_8bit, torch_dtype=torch.float16, device_map="auto")
    #     model = PeftModel.from_pretrained(model, lora_weights, torch_dtype=torch.float16)
    # elif device == "mps":
    #     model = LlamaForCausalLM.from_pretrained(base_model, device_map={"": device}, torch_dtype=torch.float16)
    #     model = PeftModel.from_pretrained(model, lora_weights, device_map={"": device}, torch_dtype=torch.float16)
    # else:
    #     model = LlamaForCausalLM.from_pretrained(base_model, device_map={"": device}, low_cpu_mem_usage=True)
    #     model = PeftModel.from_pretrained(model, lora_weights, device_map={"": device})

    # model.config.pad_token_id = tokenizer.pad_token_id = 0
    # model.config.bos_token_id = 1
    # model.config.eos_token_id = 2
    # model.half()
    # model.eval()
    # if torch.__version__ >= "2" and sys.platform != "win32":
    #     model = torch.compile(model)

    # def evaluate(instruction, input=None, temperature=0.1, top_p=0.75, top_k=40, num_beams=4, max_new_tokens=128, stream_output=False, **kwargs):
    #     prompt = prompter.generate_prompt(instruction, input)
    #     inputs = tokenizer(prompt, return_tensors="pt")
    #     input_ids = inputs["input_ids"].to(device)
    #     generation_config = GenerationConfig(
    #         temperature=temperature,
    #         top_p=top_p,
    #         top_k=top_k,
    #         num_beams=num_beams,
    #         **kwargs,
    #     )
    #     with torch.no_grad():
    #         generation_output = model.generate(
    #             input_ids=input_ids,
    #             generation_config=generation_config,
    #             return_dict_in_generate=True,
    #             output_scores=True,
    #             max_new_tokens=max_new_tokens,
    #         )
    #     s = generation_output.sequences[0]
    #     output = tokenizer.decode(s)
    #     return prompter.get_response(output)

    # Load data
    data = load_json("/PATH_TO/general-pidgin-modeling/llama/data/eval_dataset.json")
    refs_pcm = []
    hyps_pcm = []
    refs_eng = []
    hyps_eng = []
    for item in tqdm.tqdm(data[:100]):
        instruction = item["instruction"]
        input_text = item.get("input", None)
        output_text = item["output"]
        if "translate English to Nigerian Pidgin" in instruction:
            response, data_before_instruction = evaluate(instruction, input_text)
            refs_pcm.append(output_text)
            hyps_pcm.append(data_before_instruction)

        elif "translate Nigerian Pidgin to English" in instruction:
            response, data_before_instruction = evaluate(instruction, input_text)
            refs_eng.append(output_text)
            hyps_eng.append(data_before_instruction)

    # Compute BLEU score for PCM and English
    bleu_score_pcm = sacrebleu.corpus_bleu(hyps_eng, [refs_pcm])
    print(f"Bleu Score for EN2PCM: {bleu_score_pcm.score}")
    bleu_score_eng = sacrebleu.corpus_bleu(hyps_pcm, [refs_eng])
    print(f"Bleu Score for PCM2English: {bleu_score_eng.score}")

    # Save outputs
    write_txt("referencePCM100Examples.txt", "\n".join(refs_pcm))
    write_txt("pcmPreds100Examples.txt", "\n".join(hyps_eng))
    write_txt("englishReference100Examples.txt", "\n".join(refs_eng))
    write_txt("englishPreds100Examples.txt", "\n".join(hyps_pcm))

if __name__ == "__main__":
    fire.Fire(main)
