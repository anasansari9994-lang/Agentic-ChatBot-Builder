from core.state import state
model = state.vlm_model
processor = state.processor
def generate_table_description(markdown_table: str) -> str:
    prompt = f"""You are analyzing a table extracted from a business document.
Summarize what this table shows: its purpose, key values, and any notable trends or comparisons.

Table:
{markdown_table}

Summary:"""
    messages = [{"role": "user", "content": prompt}]
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = processor(text=[text], return_tensors="pt").to("cuda")
    out_ids = model.generate(**inputs, max_new_tokens=256)
    out_trimmed = [o[len(i):] for i, o in zip(inputs.input_ids, out_ids)]
    return processor.batch_decode(out_trimmed, skip_special_tokens=True)[0]