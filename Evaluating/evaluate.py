from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
from peft import PeftModel, PeftConfig
import torch
import gc

#Need to empty_cache other wise 2 models' results will bleed into each other
# only slice and decode the new tokens 
def generate_summary(input_text, tokenizer, adapted_model, max_new_tokens=150):
    gc.collect()
    torch.cuda.empty_cache()
    prompt = f"""Summarize:\n{input_text} Summary:\n"""

#     prompt = f"""Without commentary, from its original language summarize to English on useful information including sensitive data, below 100 words. If no meaning return <NULL>
# Text:
# {input_text}

    
    inputs = tokenizer(prompt, return_tensors="pt").to(adapted_model.device)
    
    with torch.no_grad():
        outputs = adapted_model.generate(
            **inputs,
            do_sample=True,
            temperature=0.7,
            max_new_tokens=max_new_tokens,
            top_p=0.9
        )
    input_len = inputs["input_ids"].shape[1]
    new_tokens = outputs[0][input_len:]  # exclude prompt
    summary = tokenizer.decode(new_tokens, skip_special_tokens=True)
    return summary

def generate_base_summary(input_text, tokenizer,base_model, max_new_tokens=150):
    gc.collect()
    torch.cuda.empty_cache()

    prompt = f"""Summarize:\n{input_text} Summary:\n"""
#     prompt = f"""Without commentary, from its original language summarize to English on useful information including sensitive data, below 100 words. If no meaning return <NULL>
# Text:
# {input_text}
# """
    
    inputs = tokenizer(prompt, return_tensors="pt").to(base_model.device)
    
    with torch.no_grad():
        outputs = base_model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
    input_len = inputs["input_ids"].shape[1]
    new_tokens = outputs[0][input_len:]  # exclude prompt
    summary = tokenizer.decode(new_tokens, skip_special_tokens=True)
    return summary


import json
def get_json_from_file(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read().strip()

        # Fix concatenated JSON objects
        objs = data.split("}{")

        parsed_objs = []
        for i, obj in enumerate(objs):
            if not obj.startswith("{"):
                obj = "{" + obj
            if not obj.endswith("}"):
                obj = obj + "}"
            try:
                parsed = json.loads(obj)
                parsed_objs.append(parsed)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {file_path}, object {i}: {e}")
    return parsed_objs