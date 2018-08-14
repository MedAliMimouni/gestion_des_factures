from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save

# Create your models here.

class Paragraphe(models.Model):
    nom = models.CharField(max_length=30)
    montant_total = models.IntegerField()
    montant_utilisé = models.IntegerField(default=0)
    def __str__(self):
        return self.nom
    def save(self):
        self.reste = self.montant_total
        super(Paragraphe, self).save()
    def restant(self):
        return self.montant_total-self.montant_utilisé

class Depense(models.Model):
    titre = models.CharField(max_length=20)
    description = models.TextField(max_length=300)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.titre


# add signal to test if there is the  amoount to transfer it
#with no edit or delete
class Facture(models.Model):
    ref_facture = models.CharField(max_length=20)
    date_facture = models.DateField(auto_now_add=True)
    montant = models.IntegerField()
    depense = models.OneToOneField(Depense,on_delete=models.CASCADE)
    paragraphe = models.ForeignKey(Paragraphe,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.depense.titre+" "+self.ref_facture
    #  a terminer
    def clean(self):
        if self.montant > self.paragraphe.restant():
            raise ValidationError(_('Le montant est plus grand que le montant reserve de '+str(self.paragraphe)))

def enregistrer_facture(sender, instance, **kwargs):
    paragraphe_relatif = instance.paragraphe
    paragraphe_relatif.montant_utilisé += instance.montant
    paragraphe_relatif.save()

post_save.connect(enregistrer_facture, sender=Facture)

class Remboursement(models.Model):
    date = models.DateField(auto_now_add=True)
    facture = models.OneToOneField(Facture,on_delete=models.CASCADE)

def enregistrer_remboursement(sender, instance, **kwargs):
    paragraphe_relatif = instance.facture.paragraphe
    paragraphe_relatif.montant_utilisé -= instance.facture.montant
    paragraphe_relatif.save()


post_save.connect(enregistrer_remboursement, sender=Remboursement)