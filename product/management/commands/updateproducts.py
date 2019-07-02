from django.core.management.base import BaseCommand, CommandError

# Third party import
import openfoodfacts

# Local import
from core.models import Product


class Command(BaseCommand):
    help = 'Update the products saved by users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--ids',
            nargs='+',
            type=int
        )

    def handle(self, *args, **options):
        if options['ids']:
            for p in options['ids']:
                if Product.objects.filter(id=p).exists():
                    self.update(p)
                    self.stdout.write(
                        self.style.SUCCESS(
                            'Successfully updated product ID "%s"' % p))
                else:
                    raise CommandError('ID "%s" is not in the database' % p)

        else:
            db_products = Product.objects.all()
            for product in db_products:
                self.update(product.id)
                self.stdout.write(
                    self.style.SUCCESS(
                        'Successfully updated product ID "%s"' % product.id))

    @staticmethod
    def update(product_id):
        p = openfoodfacts.products.get_product(str(product_id))
        off_link = 'https://fr.openfoodfacts.org/produit/'
        updated = Product(
            id=product_id,
            name=p['product']['product_name'],
            ng=p['product']['nutrition_grades'],
            img=p['product']['selected_images']['front']['display']['fr'],
            link_off=off_link + str(product_id),
            energy=p['product']['nutriments']['energy_100g'],
            fat=p['product']['nutriments']['fat_100g'],
            saturated_fat=p['product']['nutriments']['saturated-fat_100g'],
            carbohydrate=p['product']['nutriments']['carbohydrates_100g'],
            sugars=p['product']['nutriments']['sugars_100g'],
            proteins=p['product']['nutriments']['proteins_100g'],
            salt=p['product']['nutriments']['salt_100g']
        )
        updated.save()
