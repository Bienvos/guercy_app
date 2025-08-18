from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import  ListView, View, UpdateView,DetailView
from .models import fournisseurs, partenaires, produits, categories,vente,lignevente,client,Travailleurs
from .forms import ProdForm, CategoriForm,FournissForm,venteForm,ClientForm,TravailleurForm
from .fonctions import get_products
from django.template.loader import get_template
from django.http import HttpResponse
from django.contrib import messages
import logging
# from django.urls import reverse_lazy

logger = logging.getLogger(__name__)

import pdfkit


# Create your views here.

# def acceuil(request):
#     return render(request,'index.html')

class acceuil(View):

    """
    vue permettant de voir tout les prouduits 
    du stock 
    """

    template_name='dashbord_h.html'
    query = produits.objects.all()

    context = {
        'produits': query
    }


    def get(self,request,*args,**kwargs):
        return render(request, self.template_name, self.context)
    


    def post(self, request, *args,**kwargs):

        #Recherche de Produit

        # if request.POST['recherche']:
        #     res =  request.POST['recherche']
        #     print(res)

        #     print(request.POST.get('recherche'))
            
        #     donnees = produits.objects.filter(nom__icontains = request.POST.get('recherche'))
        #     self.context['donnees']=donnees

        # suppression d'un produit

        if request.POST.get('id_supprimer'):
        

            try:
                obj = produits.objects.get(pk=request.POST.get('id_supprimer'))
                obj.delete()
                # messages.success(request, " Produit Supprimer  avec Succès !!!")

            except Exception as e:
                messages.error(request , f" l'identifiant du produit n'a pas été recuperer {e}")
            

            


            


            






        return render(request, self.template_name,self.context)


# class createcate(CreateView):
#     template_name= 'createp.html'
#     Model = categories
#     form_class = CategoriForm
#     success_url = reverse_lazy('craetep')


# class Ajoutpro(CreateView):
#     template_name= 'createp.html'
#     Model = produits
#     form_class = ProdForm
#     success_url = reverse_lazy('acceuil')

class Ajoutpro(View):


    """
    vue permettant d'ajouter un produit 
    au stock mais d'ajouter un fournisseur 
    et une  categorie
    """

    template_name ='creap_personnalisee.html'


    def get(self,request, *args, **kwargs):
        form1 = ProdForm()
        form2 = FournissForm()
        form3 = CategoriForm()
        return render(request, self.template_name,{'form1':form1,'form2': form2,'form3':form3})
    

    def post(self, request, *args, **kwargs):
        form1 = ProdForm(request.POST or None)
        form2 = FournissForm(request.POST or None)
        form3 = CategoriForm(request.POST or None)

        if 'form1' in request.POST:
            form1 = ProdForm(data=request.POST)
            form2 = FournissForm()
            form3 = CategoriForm()

            if form1.is_valid():
                form1.save()
                return redirect('acceuil')
        

        if 'form2' in request.POST:
            form1 = ProdForm()
            form2 = FournissForm(data=request.POST)
            form3 = CategoriForm()

            if form2.is_valid():
                form2.save()
                return redirect('craetep')
        

        if 'form3' in request.POST:
            form1 = ProdForm()
            form2 = FournissForm()
            form3 = CategoriForm(data=request.POST)

            if form3.is_valid():
                # print(form3)
                form3.save()
                return redirect('craetep')

        return render(request, self.template_name , {'form1':form1,'form2': form2,'form3':form3})

class ModifPro(UpdateView):
    model = produits
    form_class = ProdForm
    template_name = 'modifpro.html'
    success_url= reverse_lazy('acceuil')


# def createcate(request):

#     # form1 =CategoriForm()
    

#     if request.method == "POST":
        
#         nom = request.POST.get('categorie_id')
     
#         # c = categories.objects.create(**donnes)

#         c= categories(nom=nom)
#         c.save()
        
        
#         return redirect('craetep')


#     return render (request, 'createc.html')

def ventepr(request):
    Produits = produits.objects.all()
    form = venteForm()
    form1 =ClientForm()

    if request.method =='POST':
        form1 =ClientForm(request.POST)
        form = venteForm(request.POST)

        if 'form' in request.POST:

            
            form1 =ClientForm()
            form = venteForm(request.POST)

            if form.is_valid():

                prod=[]
                prod_id= request.POST.getlist('produit')
                # print(prod_id)
                for index in prod_id:
                     el = produits.objects.get(id=index)
                     

                     prod.append(el)

                # print(prod)

                
                    # v = vente(prvoduit=prod,client=form1.client,quantite=form.quantite,prix_unitaire=prod.prix,total=prod.prix * form.quantite)
                    # v.save()
                
                qte = request.POST.getlist('quantite')
                px = request.POST.getlist('prix')
                totalp = request.POST.getlist('totalp')
                totalvente = request.POST.get('totalvente')
                clt = form.cleaned_data['client'].id

                

                # Client = client.objects.all()
                # listcl = {}

                # for c in Client:
                #     listcl[c.nom] = c.id

                # cust = listcl['clt']
                # print(cust)
                     
                

            

                
                # donnees = {
                #     'client': clt,
                #     'totalvente': totalvente
                # }

                Client = client.objects.get(id=clt)

                Ventes= vente.objects.create(client=Client, total_vente=totalvente)

                print(vente.get_vente_total())
                

                elements = []
                for index, pr in enumerate(prod):
                    data = lignevente(
                        Vente_id= Ventes.id,
                        produit = pr,
                        quantite = qte[index],
                        prix_unitaire = px[index],
                        totalp = totalp[index]
                    )

                    # code de decrémentation de la quantité du produit
                    pd = produits.objects.get(id=pr.id)
                    if int(qte[index]) <= pd.quantite:
                        pd.quantite -= int(qte[index])
                        pd.save()

                
                    elements.append(data)
                    # print(elements)
              
                lignevente.objects.bulk_create(elements)

                return redirect('listevente')

                
        
        if 'form1' in request.POST:
            form1 =ClientForm(request.POST)
            form = venteForm()

            if form1.is_valid():
                form1.save()
                return redirect('ventepr')
        
        
        

        
        
    
    else:
        form = venteForm()
        form1 =ClientForm()

    return render(request, 'vente_personnalisee.html', {'form':form,'produits':Produits,'form1':form1})



class listvent(ListView):
    template_name ='vente_liste.html'
    model = vente
    context_object_name = 'vts'
    
    # fonction permettant de passer le total des ventes dans le context
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['totalvts'] = vente.get_vente_total()
        return context

    # def get(self,request,*args,**kwargs):
    #     return render(request,self.template_name,{'totalvts': vente.get_vente_total()})

# vue sur la facture

class facture(View):
    template_name = "facture_vrai.html"
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        context = get_products(pk)

        return render(request, self.template_name, context)
    
    def post(self,request, *args, **kwargs):
        return render(request, self.template)



def generepdf(request, *args, **kwargs):
    pk = kwargs.get('pk')
    context = get_products(pk)

    template = get_template('fapdf.html')

    html = template.render(context)

    options = {
        'page-size':'Letter',
        'encoding':'UTF-8'
    }


    

    pdf = pdfkit.from_string(html,False,options=options)
    

    
    reponse = HttpResponse(pdf,content_type ='application/pdf')
    reponse['Content-Disposition']="attachement"
    return reponse



class personnel(View):
    
    template_name = 'liste_travailleurs.html'

    def get (self,request, *args, **kwargs):
        return (request, self.template_name)
    

    def post(self, request, *args, **kwargs):
        return (request, self.template_name)



def platini(request):
    return render(request,'ajouter_trav.html')

def ajout_per(request):
    return render(request,'liste_trav.html')

def ajout_travailleur(request):
    """
    Vue pour ajouter un nouveau travailleur
    """
    if request.method == 'POST':
        form = TravailleurForm(request.POST)
        if form.is_valid():
            try:
                # Sauvegarder le travailleur
                travailleur = form.save()
                
                # Message de succès
                messages.success(request, f"Le travailleur {travailleur.nom} {travailleur.prenom} a été ajouté avec succès!")
                
                # Rediriger vers la liste des travailleurs
                return redirect('listepersonnel')
                
            except Exception as e:
                # En cas d'erreur lors de la sauvegarde
                logger.error(f"Erreur lors de l'ajout du travailleur: {e}")
                messages.error(request, "Une erreur s'est produite lors de l'ajout du travailleur. Veuillez réessayer.")
        else:
            # Si le formulaire n'est pas valide, afficher les erreurs
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erreur dans le champ {field}: {error}")
    else:
        # Si c'est une requête GET, créer un formulaire vide
        form = TravailleurForm()
    
    # Contexte pour le template
    context = {
        'form': form,
        'title': 'Ajouter un Travailleur',
        'submit_text': 'Enregistrer le Travailleur',
        'cancel_url': 'liste_travailleurs'
    }
    
    return render(request, 'ajouter_trav.html', context)



def liste_travailleurs(request):
    """
    Vue pour lister tous les travailleurs
    """
    try:
        travailleurs = Travailleurs.objects.all().order_by('-date_embau')
        
        # Calculer le total des salaires
        total_salaire = sum(travailleur.salaire for travailleur in travailleurs)
        
        context = {
            'travailleurs': travailleurs,
            'total_salaire': total_salaire,
            'total_travailleurs': travailleurs.count()
        }
        
        return render(request, 'liste_trav.html', context)
        
    except Exception as e:
        logger.error(f"Erreur lors du chargement de la liste des travailleurs: {e}")
        messages.error(request, "Une erreur s'est produite lors du chargement de la liste des travailleurs.")
        return render(request, 'liste_trav.html', {'travailleurs': [], 'total_salaire': 0, 'total_travailleurs': 0})


def getcategorie(request):
    
    Ctegori =categories.objects.all()

    return render(request,'categorieser.html',{'Categorie':Ctegori})


def clients_e(request):
    cl = client.objects.all()
    return render(request, 'clients_p.html', {'clients':cl})



def fourniss(request):
    cl = fournisseurs.objects.all()
    return render(request, 'fournisseurs_p.html', {'fournisseurs':cl})


def partenai(request):

    cl = partenaires.objects.all()
    return render(request, 'partenaire_p.html', {'partenaires':cl})


class detailprod(DetailView):
    model = produits
    template_name = 'detailperso.html'
    context_object_name = 'n'







    

