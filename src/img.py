from stable_diffusion_tf.stable_diffusion import StableDiffusion
from PIL import Image

generator = StableDiffusion( 
    img_height=512,
    img_width=512,
    jit_compile=False,  # You can try True as well (different performance profile)
    download_weights=True,
)
img = generator.generate(
    "DSLR photograph of an astronaut riding a horse",
    num_steps=30,
    unconditional_guidance_scale=7.5,
    temperature=1,
    batch_size=1,
)

pil_img = Image.fromarray(img[0])
filename = f"image.png"
pil_img.save(filename)

