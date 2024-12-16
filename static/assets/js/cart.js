// Update Cart Totals
const updateCartTotal = () => {
    const cartItems = document.querySelectorAll('.cart-item');
    let subtotal = 0;
    
    cartItems.forEach(item => {
      const price = parseFloat(item.querySelector('p').textContent.replace('$', ''));
      const quantity = item.querySelector('.item-quantity').value;
      subtotal += price * quantity;
    });
  
    const shipping = subtotal > 100 ? 0 : 10; // Free shipping for orders over $100
    const total = subtotal + shipping;
  
    // Update subtotal, shipping, and total on the page
    document.getElementById('subtotal').textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById('shipping').textContent = `$${shipping.toFixed(2)}`;
    document.getElementById('total').textContent = `$${total.toFixed(2)}`;
  };
  
  // Remove Item from Cart
  const removeItem = (button) => {
    const cartItem = button.closest('.cart-item');
    cartItem.remove();
    updateCartTotal();
  };
  
  // Event Listeners
  document.querySelectorAll('.remove-item').forEach(button => {
    button.addEventListener('click', () => removeItem(button));
  });
  
  document.querySelectorAll('.item-quantity').forEach(input => {
    input.addEventListener('input', updateCartTotal);
  });
  
  // Initial Cart Total Update
  updateCartTotal();
  
  document.getElementById('addToCart').addEventListener('click', function(event) {
    event.preventDefault();
    alert('Added to the Cart');
    console.log('Added to the Cart');;
  })
  function addToCart() {
      document.getElementById('modal').style.display = "block";
      alert('added successfully!')
    }
    
let quantity = 1;
let unitPrice = 20;

function updateQuantity(amount, price) {
  quantity += amount;
  if (quantity < 1) quantity = 1; // Prevent going below 1
  document.getElementById('quantity').textContent = quantity;
  document.getElementById('subtotal').textContent = quantity * price;
  document.getElementById('total-subtotal').textContent = quantity * price;
  document.getElementById('total-price').textContent = quantity * price + 5; // Assuming $5 shipping
}

function removeItem(button) {
  button.parentElement.remove();
}



$(document).on('click', '#remove-item', function(e) {
  e.preventDefault();
  $.ajax({
      type: 'POST',
      url: "{% url 'remove_item' %}",
      data: {
          product_id: $('#remove-item').val(),
          csrfmiddlewaretoken: '{{csrf_token}}',
          action: 'post',
      },
      success: function(response) {
          addToCart()
      },
      error: function(xhr, errmsg, err){
         
      },
  })
})