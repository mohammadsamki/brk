from django.shortcuts import render
from .blockonomics import create_payment_request, verify_payment, create_invoice
from django.http import HttpResponse


def payment_callback(request):
    if request.method == 'POST':
        txid = request.POST.get('txid')
        if verify_payment(txid):
            # Payment successful, process the order
            # ...
            return HttpResponse('Payment successful')
        else:
            # Payment failed or pending, handle the error
            # ...
            return HttpResponse('Payment failed or pending')
    return HttpResponse('Invalid request')

def payment(request):
       if request.method == 'POST':
           amount = request.POST.get('amount')
           callback_url = 'https://your-website.com/payment/callback'  # Replace with your callback URL
           address, bitcoin_amount = create_payment_request(amount, callback_url)
           if address and bitcoin_amount:
               return render(request, 'payment.html', {'address': address, 'bitcoin_amount': bitcoin_amount})
           else:
               return render(request, 'error.html', {'message': 'Failed to create payment request'})
       else:
           return render(request, 'payment_form.html')
       
def invoice(request):
       amount = request.GET.get('amount')
       invoice_data = create_invoice(amount)
       if invoice_data:
           return render(request, 'invoice.html', {'invoice_data': invoice_data})
       else:
           return render(request, 'error.html', {'message': 'Failed to create invoice'})