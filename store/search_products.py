
from django.db.models import Q
from .models import Product

def search_products(keywords):
    """
    Searches for products based on given keywords.

    Args:
        keywords: A string of keywords to search for.

    Returns:
        A queryset of Product objects matching the search criteria.
    """
    
    # Split the input string into individual keywords
    keyword_list = keywords.split()
    
    # Create a Q object to combine conditions
    q = Q()

    # Iterate over each keyword and add search conditions for title and description
    for keyword in keyword_list:
        q |= Q(title__icontains=keyword) | Q(description__icontains=keyword)

    # Filter products based on the combined search criteria
    return Product.objects.filter(q)