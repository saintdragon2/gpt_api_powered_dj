from diffusers import StableDiffusionPipeline
import torch

model_id = "dreamlike-art/dreamlike-diffusion-1.0"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

prompt = "dreamlikeart, A man in walking on the street in the night with his friends."
image = pipe(prompt).images[0]

image.save("./dreamlike_diffusion/result.jpg")
