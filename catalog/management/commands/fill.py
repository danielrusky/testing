import json

from catalog.models import Category, Product, Contacts

from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        Category.objects.all().delete()
        Contacts.objects.all().delete()
        Product.objects.all().delete()

        with open('./catalog.json', 'r', encoding="utf-8") as f:
            the_list = json.loads(f.read())

        categories_to_fill = []
        contacts_to_fill = []
        products_to_fill = []
        index_for_products = {}
        for item in the_list:
            if item['model'] == 'catalog.category':
                temp = Category(**item['fields'])
                categories_to_fill.append(temp)
                index_for_products |= ({item['pk']: temp})
            elif item['model'] == 'catalog.contacts':
                tempy = Contacts(**item['fields'])
                contacts_to_fill.append(tempy)
            elif item['model'] == 'catalog.product':
                products_to_fill.append(Product(name=item['fields']['name'],
                                                description=item['fields']['description'],
                                                image=item['fields']['image'],
                                                category=index_for_products[item['fields']['category']],
                                                price=item['fields']['price'],
                                                date_created=item['fields']['date_created'],
                                                date_modified=item['fields']['date_modified'],
                                                is_active=item['fields']['is_active']))
        Category.objects.bulk_create(categories_to_fill)
        Contacts.objects.bulk_create(contacts_to_fill)
        Product.objects.bulk_create(products_to_fill)