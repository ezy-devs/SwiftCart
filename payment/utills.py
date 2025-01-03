
from Cart.models import Cart

def calculate_cart_total(request):
    """
    Calculates the total price of items in the cart for the current user or session.
    """
    total_price = 0.0
    cart = None

    # Retrieve the cart based on user authentication
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()  # Ensure session exists
            session_key = request.session.session_key
        cart = Cart.objects.filter(session_key=session_key).first()

    # If no cart or no items in cart, return None
    if not cart or not cart.items.exists():
        return None

    # Calculate total price
    for item in cart.items.all():
        price = item.product.sale_price if item.product.is_sale else item.product.price
        total_price += item.quantity * float(price)

    return round(total_price, 2)  # Return total price rounded to 2 decimal places



# def calculate_cart_total(request):
#     """
#     Calculates the total price of items in the cart for the current user or session.
#     """
#     total_price = 0.0
#     cart = None

#     if request.user.is_authenticated:
#         cart = Cart.objects.filter(user=request.user).first()
#     else:
#         session_key = request.session.session_key
#         if session_key:
#             cart = Cart.objects.filter(session_key=session_key).first()

#     if not cart or not cart.items.exists():
#         return None

#     for item in cart.items.all():
#         price = item.product.sale_price if item.product.is_sale else item.product.price
#         total_price += item.quantity * float(price)

#     return total_price
