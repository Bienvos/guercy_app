from django.db import models
from django.db.models import Sum

# Create your models here.

FONCTION_CHOICES = [
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

type_renum = [
    ('mois','Mois'), ('jour','Jour'),('semaine','Semaine')
]

choix = [
    ('cahe','Cahe'),
    ('transfere Bancaire','Transfère Bancaire')
]

class categories(models.Model):
    nom=models.CharField(max_length = 50)
    
    
    def __str__(self):
        return self.nom

class fournisseurs(models.Model):
    nom = models.CharField(max_length = 100)
    prenom = models.CharField(max_length = 100)
    contact = models.CharField(max_length=12)
    email = models.EmailField()
    Adresse = models.CharField(max_length = 50)
    mode_payement = models.CharField( max_length = 18, choices = choix)

    def __str__(self):
        return f"{self.nom} {self.prenom} "
    



class produits(models.Model):
    nom = models.CharField(max_length =100)
    categorie = models.ForeignKey(categories, on_delete = models.CASCADE, related_name ='products')
    prix = models.DecimalField(max_digits = 10 , decimal_places =2)
    quantite = models.PositiveIntegerField()
    description = models.TextField()
    date_livraison = models.DateField()
    date_ajout = models.DateTimeField(auto_now_add = True)
    data_exp = models.DateField(null =True , blank = True)
    fournisseur = models.ForeignKey(fournisseurs,on_delete=models.CASCADE)
    observation = models.TextField()
    # vente = models.ManyToManyField(vente , related_name ="vpp")
    # image = models.ImageField(null =True , blank = True, upload_to ='/media')

    class Meta:
        ordering = ['-date_ajout']


    def status(self):
        if self.quantite == 0:
            return "faible"

        elif self.quantite <= 10:
            return "moyen"

        else:
            return "eleve"
    
    @property
    def get_total(self):
        total = float(self.quantite) * self.prix
        return total
    
    def __str__(self):
        return self.nom


class client (models.Model):
    nom = models.CharField(max_length = 100)
    # prenom = models.CharField(max_length=100)
    Tel = models.CharField(max_length = 13)
    # adresse = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nom


class partenaires(models.Model):
    nom = models.CharField(max_length = 100)
    prenom = models.CharField(max_length = 100)
    produit = models.ForeignKey(produits , on_delete= models.CASCADE, related_name ='avis')
    observation = models.TextField()
    fournisseur = models.ManyToManyField(fournisseurs)

    def __str__(self):
        return f"{self.nom} {self.prenom} "







class vente (models.Model):
    # produit = models.ForeignKey(produits, on_delete = models.CASCADE, related_name ='vp')
    # facture = models.OneToOneField(Facture,on_delete = models.CASCADE,related_name='ventes')
    date_achat = models.DateTimeField(auto_now_add =True)
    # quantite = models.PositiveIntegerField()
    # prix_unitaire =models.DecimalField(max_digits=10, decimal_places = 2)
    client = models.ForeignKey(client , on_delete =models.PROTECT)
    # total_a = models.DecimalField(max_digits =10 , decimal_places = 2)
    total_vente = models.DecimalField(max_digits=10, decimal_places =2)

    class Meta:
        ordering = ['-date_achat']
    
    @classmethod
    def get_vente_total(cls):
        total = cls.objects.aggregate(somme = Sum('total_vente'))['somme']
        return total or 0

    @property
    def get_total(self):
        prod= self.total_vente
        total = sum(p.get_total for p in prod)
        return total

    def __str__(self):
        return f"{self.client}_ {self.date_achat}"


class lignevente(models.Model):
    Vente = models.ForeignKey(vente , on_delete = models.CASCADE, related_name='Lignes')
    produit = models.ForeignKey(produits, on_delete = models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    totalp = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.produit.nom} - {self.Vente.client} "

    


class Facture (models.Model):
    # client = models.ForeignKey(client , on_delete = models.CASCADE)// a supprimer
    
    produit = models.ForeignKey(produits, on_delete =models.CASCADE)
    Vente =models.OneToOneField(vente, on_delete = models.CASCADE)
    quantite = models.PositiveIntegerField()
    date_ach = models.DateTimeField(auto_now_add =False)

    def __str__(self):
        return f" reçu de {self.Vente.client} "






class Travailleurs(models.Model):
    nom = models.CharField(max_length = 100)
    prenom = models.CharField(max_length = 100)
    date_naiss =models.DateField()
    contacts =models.CharField(max_length = 30)
    date_embau=models.DateField()
    jour_travailler= models.PositiveIntegerField()
    jour_absen= models.PositiveIntegerField()
    observation = models.TextField()


    fonction = models.CharField(max_length = 100,choices=FONCTION_CHOICES)
    renumere_par = models.CharField(max_length=18,choices = type_renum)
    salaire = models.DecimalField(max_digits =20,decimal_places =2)

    @property
    def net(self):
        payer = self.salaire * self.jour_travailler
        return payer

    def __str__(self):
        return f"{self.nom}_{self.prenom}"
    





