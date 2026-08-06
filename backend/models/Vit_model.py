from transformers import Qwen2_5_VLForConditionalGeneration, BitsAndBytesConfig, AutoProcessor
import torch
import time

def load_vlm():
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        "Qwen/Qwen2.5-VL-3B-Instruct",
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
    )

    processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-3B-Instruct")
    return model, processor