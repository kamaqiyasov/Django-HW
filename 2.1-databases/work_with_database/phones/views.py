from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    sort_by = request.GET.get('sort', False)
    template = 'catalog.html'
    phones_obj = Phone.objects.all()
    SORT_MAPPING = {
        'min_price': 'price',
        'max_price': '-price',
        'name': 'name'
    }
    if sort_by:
        sort_field = SORT_MAPPING.get(sort_by, 'name')
        phones_obj = phones_obj.order_by(sort_field)
    
    context = {
        'phones': phones_obj
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone_obj = Phone.objects.get(slug=slug)
    context = {
        'phone': phone_obj
    }
    return render(request, template, context)
