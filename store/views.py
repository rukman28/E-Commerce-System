from django.shortcuts import render, get_object_or_404

from store.models import Product

import base64

from .tasks import generate_caption_for_search

from .search_products import search_products

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

# Create your views here.
def index(request):
    
    # Get all products from the database
    all_products = Product.objects.all()

    # Pass the products to the template context
    context = {'products': all_products}

    return render(request, 'store_home.html', context)

def all_products(request):
    # Get all products from the database
    all_products = Product.objects.all()
    
    # Pass the products to the template context
    context = {'products': all_products}
    
    return render(request, 'all_products.html', context)

def product_detail(request, product_id):
    # Get the product with the specified ID
  product = get_object_or_404(Product, pk=product_id)

  # Pass the product to the template context
  context = {'product': product}

  return render(request, 'product_detail.html', context)
    
@csrf_exempt
def search_by_image(request):
  if request.method == 'POST':
    try:
      data = json.loads(request.body)
      image_data_base64 = data['image_data']
      search_keywords = generate_caption_for_search(image_data_base64)
      if search_keywords:
        products = search_products(search_keywords)
        print("The found products type is ", type(products))
        # ... prepare search results data (e.g., product information)
        results_data = {  # Replace with your product data formatting
          "products": [
            {"title": product.title, "description": product.description, "image": f"{settings.MEDIA_URL}/{product.image}", "price": product.price}
            for product in products
          ]
        }
        print("The search by image result is ",results_data)
        return JsonResponse(results_data)
      else:
        return JsonResponse({'error': 'Failed to generate keywords from the image.'})
    except Exception as e:
      print(f"Error processing image search request: {e}")
      return JsonResponse({'error': 'An error occurred during search.'})
  else:
    return JsonResponse({'error': 'Invalid request method.'})