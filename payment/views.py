from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ShippingForm
from .models import ShippingInfo


def update_shipping_info(request):
    if request.user.is_authenticated:
        shipping_info = ShippingInfo.objects.filter(user=request.user).first()

    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        shipping_info = ShippingInfo.objects.filter(session_key=session_key).first()

    if request.method == 'POST':
        form = ShippingForm(request.POST, instance=shipping_info)
        if form.is_valid():
            shipping_instance = form.save(commit=False)
            if request.user.is_authenticated:
                shipping_instance.user = request.user
            else:
                shipping_instance.session_key = request.session.session_key
            shipping_instance.save()
            
            messages.success(request, 'Shipping info updated successfully!')
            # return redirect('profile', request.user.username if request.user.is_authenticated else 'guest')
            return redirect(update_shipping_info)
        else:
            messages.error(request, 'could not process request, try again!')
            return redirect(update_shipping_info)
    else:
        form = ShippingForm(instance=shipping_info)

    return render(request, 'payment/shipping_form.html', {'form': form})




def payment_success(request):
    pass

