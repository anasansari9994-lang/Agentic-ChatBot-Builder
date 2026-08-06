from core.state import state
model = state.vlm_model
processor = state.processor
def describe_chart(image_path: str) -> str:
    messages = [{
        "role": "user",
        "content": [
            {"type": "image", "image": image_path},
            {"type": "text", "text": "Describe this chart/table in detail: axis labels, key values, trends, and comparisons. Be specific with numbers."}
        ]
    }]
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(text=[text], images=image_inputs, videos=video_inputs, padding=True, return_tensors="pt").to("cuda")
    out_ids = model.generate(**inputs, max_new_tokens=512)
    out_trimmed = [o[len(i):] for i, o in zip(inputs.input_ids, out_ids)]
    return processor.batch_decode(out_trimmed, skip_special_tokens=True)[0]