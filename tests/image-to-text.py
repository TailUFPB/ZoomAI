import os
import io
import base64 
from PIL import Image

from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to("cuda")

text = "a photography of"

image_url = "./city_night.jpeg"
raw_image = Image.open(image_url).convert('RGB')

#inputs = processor(raw_image, text, return_tensors="pt").to("cuda")

# out = model.generate(**inputs)
# print(processor.decode(out[0], skip_special_tokens=True))

# unconditional image captioning

inputs = processor(raw_image, return_tensors="pt").to("cuda")

out = model.generate(**inputs, max_new_tokens=1000)
print(processor.decode(out[0], skip_special_tokens=True))

