import replicate
from celery import shared_task
from .models import Product
import base64
from django.conf import settings
import os
import cloudinary
from cloudinary import CloudinaryImage

import cloudinary
from cloudinary.uploader import upload_image
from cloudinary.utils import cloudinary_url
from celery import chain
import requests
import PIL.Image as Image
import io
from django.core.files import File

import json

from langchain_google_genai.llms import GoogleGenerativeAI
from .generate_product_description import ProductDescriptionGenerator

import time
import random

from .search_products import search_products

def run_product_description_generation_via_gemini(generated_text_from_image):
    llm = GoogleGenerativeAI(model="gemini-1.0-pro", google_api_key=os.environ.get('GOOGLE_AI_STUDIO_API_KEY'))
    chain = ProductDescriptionGenerator.from_llm(llm, verbose=True)
    return chain.invoke({"extracted_text": generated_text_from_image})

@shared_task
def upload_to_cloudinary(data):
    
    product_id = data['product_id']

    # Decode base64 data to bytes
    byte_data = base64.b64decode(data['image'].encode('utf-8'))
        
    upload_result = cloudinary.uploader.upload(
        file=byte_data,
        public_id="clothing_item",
        unique_filename = False, 
        overwrite=True,
    )
    
    srcURL = CloudinaryImage("clothing_item").build_url()
    
    print(srcURL)
    
    # Get the secure URL of the uploaded image
    secure_url = upload_result.get('secure_url')
    print("Secure URL ", secure_url)
    
    # Chain the generate_caption task with the result
    return chain(generate_caption.s(srcURL, product_id)).delay()

@shared_task
def generate_caption(image_url, product_id):
    
    product = Product.objects.get(id=product_id)
    
    print("Image Path: " + image_url)
    
    base_delay = 2  # Base delay in seconds
    max_retries = 3  # Define the maximum number of retries

    for attempt in range(1, max_retries + 1):
        try:
            output = replicate.run(
                "rmokady/clip_prefix_caption:9a34a6339872a03f45236f114321fb51fc7aa8269d38ae0ce5334969981e4cd8",
                input={
                    "image": image_url,
                    "model": "conceptual-captions",
                    "use_beam_search": False
                }
            )
            try:
                result = run_product_description_generation_via_gemini(output)
                result = result['text'].strip('\n')
                
                # Extract JSON content
                json_content = result[result.find('{'):result.rfind('}')+1]

                # Parse JSON
                data = json.loads(json_content)

                print(f"Generated Product Description ", data)
                
                product.description = data['description']
                product.save()
            except Exception as e:
                print(f"Error generating product description in the Langchain stage: {e}")
                # Handle the error (e.g., log the error and continue)
                return

            
        except (Exception) as e:
            print(f"Attempt {attempt}: Error - {type(e).__name__} - {e}")
            if attempt < max_retries:
                delay = base_delay * 2**attempt + random.uniform(0, 1)  # Exponential backoff with randomization
                print(f"Waiting {delay:.2f} seconds before retry...")
                time.sleep(delay)
            else:
                print(f"Maximum retries reached ({max_retries}). Giving up.")

        # Process the output (if successful)
    
@shared_task
def generate_caption_for_search(image_data):
    
    # Decode the base64 image data to bytes
    byte_data = base64.b64decode(image_data.encode('utf-8'))
    
    # Encode the bytes back to base64 to pass to the replicate API
    base64_image = base64.b64encode(byte_data).decode('utf-8')
    
    base_delay = 2  # Base delay in seconds
    max_retries = 3  # Define the maximum number of retries

    for attempt in range(1, max_retries + 1):
        try:
            print("Running Replicate to get the image captions.")
            output = replicate.run(
                "rmokady/clip_prefix_caption:9a34a6339872a03f45236f114321fb51fc7aa8269d38ae0ce5334969981e4cd8",
                input={
                    "image": "data:image/jpeg;base64," + base64_image,
                    "model": "conceptual-captions",
                    "use_beam_search": False
                }
            )
            try:
                print(f"Extracted captions from the image search", output)
                
                return output
            except Exception as e:
                print(f"Error extracting captions from the image search: {e}")
                # Handle the error (e.g., log the error and continue)
                return
            
        except (Exception) as e:
            print(f"Attempt {attempt}: Error - {type(e).__name__} - {e}")
            if attempt < max_retries:
                delay = base_delay * 2**attempt + random.uniform(0, 1)  # Exponential backoff with randomization
                print(f"Waiting {delay:.2f} seconds before retry...")
                time.sleep(delay)
            else:
                print(f"Maximum retries reached ({max_retries}). Giving up.")
                
