from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
import ast

# Third party import
import openfoodfacts

# Local import
from core.models import Product
from .input import UserInput
from .substitute import SubstituteQueries
from .refine import RefineSubstitute


# Create your views here.

def search(request):
    # p = product(s). sub = substitute(s). qry = query(ies).
    qry = request.GET.get('query')
    if qry:  # User's query
        user_query = UserInput(qry)
        p_param = user_query.get_product()

        if p_param:  # Product to replace
            sub_qry = SubstituteQueries(p_param)
            advanced_search = sub_qry.query_off()
            if advanced_search:  # Possible substitute
                head_p = sub_qry.get_head_product(advanced_search)
                p = sub_qry.get_substitute(advanced_search)

                if p:  # Substitutes
                    refine = RefineSubstitute(p)
                    sub = refine.product_infos()
                    context = {
                        'name': qry,
                        'substitute': sub
                    }
                    if head_p:
                        context.update({'img': head_p['img']})

                    return render(request, 'product/search.html', context)
    # Any sub, product or request
    context = {'name': "Aucun résultat"}
    return render(request, 'product/search.html', context)


def save(request):
    # p = product(s).
    # Convert request.GET string to list with ast.literal_eval()
    sub = ast.literal_eval(request.GET.get('substitute'))
    if request.user.is_authenticated:
        current_user = request.user.id
        sub_id = sub['id']
        if Product.objects.filter(id=sub_id, users=current_user).exists():
            data = {
                'success': False,
                'message': 'Le produit "' + sub['name'] +
                           '" est déjà associé à votre compte'
            }
        else:
            """
            'p' will erase previously stored value for a given (id) product
            It will conserve ManyToMany relation
            The user requesting the save will be added alongside with past one
            It act as an update for the DataBase
            """
            p = Product(
                id=sub['id'],
                name=sub['name'],
                ng=sub['ng'],
                img=sub['img'],
                link_off=sub['link_off'],
                energy=sub['energy'],
                fat=sub['fat'],
                saturated_fat=sub['saturated_fat'],
                carbohydrate=sub['carbohydrate'],
                sugars=sub['sugars'],
                proteins=sub['proteins'],
                salt=sub['salt'],
            )
            p.save()
            p.users.add(current_user)
            data = {
                'success': True,
                'message': 'Le produit "' + sub['name'] +
                           '" a bien été ajouté à votre compte'
            }
    else:
        data = {
            'success': False,
            'message': "Veuillez vous connecter avant d'enregistrer un produit"
        }
    return JsonResponse(data)


def user(request):
    # sub = substitute(s).
    if request.user.is_authenticated:
        sub = Product.objects.filter(users=request.user.id)
        context = {
            'login': True,
            'substitute': sub
        }
        return render(request, 'product/user.html', context)
    else:
        return HttpResponseRedirect('/accounts/login')


def detail(request, product_id):
    # p = product(s).
    if Product.objects.filter(id=product_id).exists():
        # fetch product detail in DB
        p = Product.objects.get(id=product_id)
        try:
            p.energy = p.energy.normalize()
            p.fat = p.fat.normalize()
            p.saturated_fat = p.saturated_fat.normalize()
            p.carbohydrate = p.carbohydrate.normalize()
            p.sugars = p.sugars.normalize()
            p.proteins = p.proteins.normalize()
            p.salt = p.salt.normalize()
            context = {'product': p}
        except AttributeError:
            context = {'product': p}
    else:
        # fetch product detail on OpenFoodFacts
        p = openfoodfacts.products.get_product(str(product_id))
        off_link = 'https://fr.openfoodfacts.org/produit/'
        context = {'product': {
            'name': p['product']['product_name'],
            'ng': p['product']['nutrition_grades'],
            'img': p['product']['selected_images']['front']['display']['fr'],
            'link_off': off_link + str(product_id),
            'energy': p['product']['nutriments']['energy_100g'],
            'fat': p['product']['nutriments']['fat_100g'],
            'saturated_fat': p['product']['nutriments']['saturated-fat_100g'],
            'carbohydrate': p['product']['nutriments']['carbohydrates_100g'],
            'sugars': p['product']['nutriments']['sugars_100g'],
            'proteins': p['product']['nutriments']['proteins_100g'],
            'salt': p['product']['nutriments']['salt_100g']
        }}
    return render(request, 'product/detail.html', context)
