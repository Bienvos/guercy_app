from django import forms
from .models import produits,categories, fournisseurs, client,vente,Travailleurs


class ProdForm(forms.ModelForm):
    class Meta:
        model = produits
        fields = ['nom','prix','quantite', 'date_livraison', 'description','categorie', 'fournisseur']

        widgets = {
            'nom':forms.TextInput( attrs={
                'placeholder': 'Entez le libéllé du Produit',
                'class':'form-control'

            }),

            'categorie':forms.Select(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Choisissez la Catégorie'

                }
            ),
            'prix': forms.NumberInput(
                attrs ={
                    'placeholder': 'Entrez le Prix Unitaire',
                    'class'      : 'form-control'
                }
            ),
            'quantite':forms.NumberInput(attrs ={
                'placeholder':'Entrez la quantite',
                'class': 'form-control'
            }),
            'description':forms.Textarea(attrs = {
                'rows':8,
                'cols':109,
                'class':'form-control',
                'placeholder':' Entrez une Description du Produit'
            }),
            'date_livraison':forms.DateInput(
                attrs ={
                    'placeholder':'Entrez la date de livraison Jour/Mois/Anne',
                    'class':'form-control',
                    'type':'date'
                }
            ),

            'fournisseur': forms.Select(
                attrs={
                    'class':'form-control'
                }
            )
        }

    # cette fonction permet de passer un message sur le champ des categories et fournisseurs
    def __init__(self,*args,**kwargs):
        super(ProdForm,self).__init__(*args,**kwargs)
        self.fields['categorie'].empty_label = "Selectionnez la Categorie "
        self.fields['fournisseur'].empty_label ="Selectionnez le Fournisseur"


class CategoriForm(forms.ModelForm):
    class Meta:
        model = categories
        fields = ['nom']

        widgets ={
            'nom': forms.TextInput(
                attrs = {
                    'placeholder':'Entrez le nom de la categorie',
                    'class':'form-control'
                }
            )
        }


class FournissForm(forms.ModelForm):
    class Meta:
        model = fournisseurs
        fields =['nom','prenom','contact','email','Adresse','mode_payement']

        widgets ={
            'nom':forms.TextInput(
                attrs ={
                    'class':'form-control',
                    'placeholder':'Entrez le nom(s) du fournisseur'
                }
            ),
            'prenom':forms.TextInput(
                attrs ={
                    'class':'form-control',
                    'placeholder':'Entrez le/les Prénom(s) du fournisseur'
                }
            ),

            'contact':forms.TextInput(
                attrs ={
                    'class':'form-control',
                    'placeholder':'Entrez le/les conctat(s) du fournisseur'
                }
            ),
            'email':forms.TextInput(
                attrs ={
                    'class':'form-control',
                    'placeholder':'Entrez le mail du fournisseur'
                }
            ),
            'Adresse':forms.TextInput(
                attrs ={
                    'class':'form-control',
                    'placeholder':'Entrez l\'Adresse du fournisseur'
                }
            ),

            'mode_payement':forms.Select(
                attrs ={
                    'class':'form-control',
        
                }
            ),

        }

    def __init__(self,*args,**kwargs):

            super(FournissForm,self).__init__(*args,**kwargs)

            self.fields['mode_payement'].empty_label = "veuillez selectionnez un mode "

class ClientForm(forms.ModelForm):
    class Meta:
        model = client
        fields =['nom', 'Tel']
        widgets ={
            'nom':forms.TextInput(attrs ={
                'class':'form-control',
                'placeholder':'Entrez le Nom du Client'
            }),

            # 'prenom':forms.TextInput(attrs ={
            #     'class':'form-control',
            #     'placeholder':'Entrez le Prenom du Client'
            # }),
            'Tel':forms.TextInput(attrs ={
                'class':'form-control',
                'placeholder':'Entrez le Numero de téléphone '
            }),

            # 'Adresse':forms.TextInput(attrs ={
            #     'class':'form-control',
            #     'placeholder':'Entrez l\'adresse du Client '
            # }),

        }

class venteForm(forms.ModelForm):
    
    class Meta:
        model = vente
        fields =['client']

        widgets ={
            'client': forms.Select( attrs={'id':'id_client',
                'class':'form-control'
            }),

            
        }

    def __init__(self,*args,**kwargs):

            super(venteForm,self).__init__(*args,**kwargs)

            self.fields['client'].queryset = client.objects.all()
            self.fields['client'].empty_label = "Veuillez selectionner un client"




class TravailleurForm(forms.ModelForm):
    class Meta:
        model = Travailleurs
        fields = [
            'nom', 'prenom', 'date_naiss', 'contacts', 'date_embau',
            'fonction', 'salaire', 'renumere_par', 'jour_travailler',
            'jour_absen', 'observation'
        ]
        
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le nom de famille',
                'required': True
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le prénom',
                'required': True
            }),
            'date_naiss': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'contacts': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1234567890',
                'required': True
            }),
            'date_embau': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'fonction': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'salaire': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
                'required': True
            }),
            'renumere_par': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'jour_travailler': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0',
                'required': True
            }),
            'jour_absen': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0',
                'required': True
            }),
            'observation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '4',
                'placeholder': 'Entrez des observations ou commentaires sur le travailleur...'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super(TravailleurForm, self).__init__(*args, **kwargs)
        # Ajouter des options pour la fonction
        self.fields['fonction'].choices = [
            ('', 'Sélectionnez une fonction'),
            ('Manager', 'Manager'),
            ('Employé', 'Employé'),
            ('Stagiaire', 'Stagiaire'),
            ('Directeur', 'Directeur'),
            ('Secrétaire', 'Secrétaire'),
            ('Comptable', 'Comptable'),
            ('Technicien', 'Technicien'),
            ('Vendeur', 'Vendeur'),
            ('Autre', 'Autre'),
        ]
        
        
        # Configurer les labels
        self.fields['nom'].label = 'Nom'
        self.fields['prenom'].label = 'Prénom'
        self.fields['date_naiss'].label = 'Date de Naissance'
        self.fields['contacts'].label = 'Contact'
        self.fields['date_embau'].label = 'Date d\'Embauche'
        self.fields['fonction'].label = 'Fonction'
        self.fields['salaire'].label = 'Salaire'
        self.fields['renumere_par'].label = 'Type de Rémunération'
        self.fields['jour_travailler'].label = 'Jours Travaillés'
        self.fields['jour_absen'].label = 'Jours Absents'
        self.fields['observation'].label = 'Observations'
        self.fields['fonction'].empty_label = "veuillez selectionnez une fonction "
        self.fields['renumere_par'].empty_label = " Mode de Paiement "
    
    def clean_contacts(self):
        contacts = self.cleaned_data.get('contacts')
        # Nettoyer le numéro de téléphone
        contacts = ''.join(filter(str.isdigit, contacts))
        if len(contacts) < 8:
            raise forms.ValidationError("Le numéro de téléphone doit contenir au moins 8 chiffres.")
        return contacts
    
    def clean_date_naiss(self):
        date_naiss = self.cleaned_data.get('date_naiss')
        if date_naiss:
            from datetime import date
            today = date.today()
            age = today.year - date_naiss.year - ((today.month, today.day) < (date_naiss.month, date_naiss.day))
            if age < 16:
                raise forms.ValidationError("L'âge minimum requis est de 16 ans.")
            if age > 100:
                raise forms.ValidationError("Veuillez vérifier la date de naissance.")
        return date_naiss
    
    def clean_date_embau(self):
        date_embau = self.cleaned_data.get('date_embau')
        if date_embau:
            from datetime import date
            today = date.today()
            if date_embau > today:
                raise forms.ValidationError("La date d'embauche ne peut pas être dans le futur.")
        return date_embau
                
    
        
    
 

    

