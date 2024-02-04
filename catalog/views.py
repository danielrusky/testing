from django.shortcuts import render, redirect

from catalog.models import Product, Category, Contacts


def home(request):
    product_list = Product.objects.all()
    context = {
        'object_list': product_list,
        'title': 'Главная'
    }
    return render(request, 'catalog/home.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        Contacts.objects.create(name=name, phone=phone, message=message)
        print(f'У вас новое сообщение от: {name}(телефон:{phone}): {message}')
    context = {
        'title': 'Контакты'
    }
    return render(request, 'catalog/contacts.html', context)


def product(request, pk):
    return render(request, 'catalog/product.html', {'product': Product.objects.get(pk=pk)})


def create_category(request):
    if request.method == 'POST':
        cat_name = request.POST.get('cat_name')
        cat_desc = request.POST.get('cat_desc')
        Category.objects.create(name=cat_name, description=cat_desc)
        return redirect('catalog:home')
    return render(request, 'catalog/create_category.html')


def create_product(request):
    if request.method == 'POST':
        prod_category = request.POST.get('prod_category')
        name = request.POST.get('prod_name')
        price = request.POST.get('prod_price')
        description = request.POST.get('prod_desc')
        prod_image = request.FILES.get('prod_image')
        Product.objects.create(name=name, description=description, price=price,
                               image=prod_image, category=Category.objects.get(id=prod_category))
        print(f"Данные:\n"
              f"Название: {name}\n"
              f"Описание: {description}\n"
              f"Цена: {price}\n"
              f"Фото: {prod_image}\n"
              f"Категория: {prod_category}")
    return render(request, 'catalog/create_product.html', {'categories': Category.objects.all()})


def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} {email} {message}')
    return render(request, 'catalog/index.html')
