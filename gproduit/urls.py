from django.urls import path
from .views import acceuil,Ajoutpro, fourniss, partenai,ventepr,listvent,facture,generepdf, personnel,platini,ajout_per,ajout_travailleur,liste_travailleurs, getcategorie, clients_e


urlpatterns = [
    path('', acceuil.as_view(), name ='acceuil'),
    path('ajout/',Ajoutpro.as_view(), name ='craetep'),
    path('vente/',ventepr, name ='ventepr'),
    path('listevente/', listvent.as_view(), name='listevente'),
    path('facture/<int:pk>/',facture.as_view(), name ="vuefacture" ),
    path("<int:pk>/", generepdf, name="facture_vrai"),
    path('personnel/', personnel.as_view(), name = "personnel" ),
    path('platini/', platini, name="platini"),
    path('ajouterpersonnel/', ajout_per, name="ajouter_personnel"),
    path('ajoutravailleur/', ajout_travailleur, name="ajoutravailleur"),
    path('listepersonnel/', liste_travailleurs, name="listepersonnel"),
    path('categorie/', getcategorie, name="categorie"),
    path('clients/', clients_e, name="clients"),
    path('fournisseurs/', fourniss, name="fournisseurs"),
    path('partenaires/', partenai, name="partenaires"),
    # path('categori/',createcate.as_view() , name="catego"),
]

