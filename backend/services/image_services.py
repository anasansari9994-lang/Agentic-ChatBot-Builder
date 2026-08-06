import torch
from models.Vit_model import processor, model, device
from PIL import Image

def generate_description(image_path: str):
    image = Image.open(image_path).convert("RGB")
    
    inputs = processor(
        text = "<DETAILED_CAPTION>",
        images= image,
        return_tensor = "pt"
    )

    input = {k: v.to(device) for k,v in inputs.items()}

    with torch.no_grad():
        generate_ids = model.generate(
            **inputs,
            max_new_tokens=512
        )

    return processor.batch_decode(
        generate_ids,
        skip_special_tokens=True
    )[0]
    

