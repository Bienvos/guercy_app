from .models import vente 


def get_products(pk):
    obj = vente.objects.get(pk=pk)
    prod = obj.Lignes.all

    context = {
        'obj':obj,
        'produits':prod
    }

    return context
