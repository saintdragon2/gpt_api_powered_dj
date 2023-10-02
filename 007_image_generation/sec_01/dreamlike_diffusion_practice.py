from diffusers import StableDiffusionPipeline
import torch

model_id = "dreamlike-art/dreamlike-diffusion-1.0"

pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

# prompt = "dreamlikeart, A rich man driving Ferrari in New York and many people are watching him, In style of by Jordan Grimmer and greg rutkowski, crisp lines and color, complex background, particles, lines, wind, concept art, sharp focus, vivid colors"
prompt = "dreamlikeart, 'Beat It' by Michael Jackson is an energetic pop/rock song with lyrics about standing up against violence and conflict, creating a powerful and determined mood."
image = pipe(prompt).images[0]

image.save("./result.jpg")
