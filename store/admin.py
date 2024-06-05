from django.contrib import admin

# Register your models here.
from .models import Product, ProductCategory

from .tasks import generate_caption, upload_to_cloudinary

import requests
import base64

class ProductAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            # Call the Celery task to generate the caption
            image_url = obj.image.url
            
            # Download the image data
            response = requests.get("http://127.0.0.1:8000"+obj.image.url, stream=True)
            
            # Check for successful response
        if response.status_code == 200:
            # Read the image data in chunks
            image_chunks = []
            for chunk in response.iter_content(1024):
                image_chunks.append(chunk)
            
            # Combine chunks and decode as bytes
            image_data = b''.join(image_chunks)
            
            # Encode image data to base64 string
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            data = {
            'product_id': obj.id,
            'image': base64_image,
            'name': obj.image.name,
            }
            
            upload_to_cloudinary.delay(data)
            
        else:
            print(f"Error downloading image: {response.status_code}")
            
            
            


admin.site.register(Product, ProductAdmin)

#admin.site.register(Product)
admin.site.register(ProductCategory)