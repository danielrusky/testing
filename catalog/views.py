from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, ListView, DeleteView, DetailView

from catalog.forms import ProductForm, CategoryForm, VersionForm, VersionCategoryForm
from catalog.models import Product, Category, Version, VersionCategory


class ProductListView(ListView):
    model = Product
    extra_context = {
        'title': 'Главная страница',
    }
    template_name = 'catalog/product_list.html'

    def get_queryset(self, *args, **kwargs):
        # QuerySet — это набор объектов из базы данных, который
        # может использовать фильтры для ограничения результатов
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_active=True)
        return queryset


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list_product')

    def form_valid(self, form):
        # проверка валидации (только create и update)
        # создаем форму, но не отправляем его в БД, пока просто держим в памяти
        # создаем переменную, сохраням и с ней работаем
        # Через реквест передаем недостающую форму, которая обязательна
        # сохраняем в базу данных
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductDetailView(DetailView):
    model = Product
    extra_context = {
        'title': 'Товар',
    }
    template_name = 'catalog/product_detail.html'


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list_product')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:list_product')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return super().form_valid(form.errors)


def toggle_active(request, slug):
    products = get_object_or_404(Product, slug=slug)
    if products.to_publish:
        products.to_publish = False
    else:
        products.to_publish = True
    products.save()
    return redirect('catalog:base', slug=products.slug)


class CategoryListView(ListView):
    model = Category
    extra_context = {
        'title': 'Категории',
    }
    template_name = 'catalog/category_list.html'


class CategoryCreateView(CreateView):
    model = Category
    fields = ('name', 'description', 'image')
    success_url = reverse_lazy('catalog:list_category')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class CategoryDetailView(DetailView):
    model = Category
    extra_context = {
        'title': 'Категория',
    }
    template_name = 'catalog/category_detail.html'


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ('name', 'description', 'image')
    success_url = reverse_lazy('catalog:list_category')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionCategoryFormset = inlineformset_factory(Category, VersionCategory, form=VersionCategoryForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionCategoryFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionCategoryFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('catalog:list_category')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return super().form_valid(form.errors)


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'
    extra_context = {
        'title': 'Контакты',
    }

    def post(self, request, *args, **kwargs):
        # POST — это запрос, который используется для отправки данных
        # на сервер. Обычно он содержит в своём теле данные, которые
        # предполагается сохранить
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'name: {name}, phone: {phone}, message: {message}')
        return render(request, 'catalog/contacts.html', self.extra_context, {'contacts': Contacts.objects.get(pk=1)})


def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} {email} {message}')
    return render(request, 'catalog/index.html')
