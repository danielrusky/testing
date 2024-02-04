from django.contrib import admin

from catalog.models import Product, Category, Contacts, Version, VersionCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('version_name', 'version_number', 'product', 'is_current')


@admin.register(VersionCategory)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('version_name', 'version_number', 'category', 'is_current')


admin.site.register(Contacts)
