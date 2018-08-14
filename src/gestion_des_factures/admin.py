from django.contrib import admin
from .models import Paragraphe, Depense, Facture, Remboursement
# Register your models here.

# admin.site.register(Paragraphe)
admin.site.register(Depense)
# admin.site.register(Facture)
admin.site.register(Remboursement)


@admin.register(Paragraphe)
class ParagrapheAdmin(admin.ModelAdmin):
    list_display = ["nom","montant_total","montant_utilisé","reste"]
    def restant(self,obj):
        return obj.montant_total-obj.montant_utilisé
    
    reste = restant

@admin.register(Facture)
class ParagrapheAdmin(admin.ModelAdmin):
    list_display = ["ref_facture","date_facture","montant","remboursée"]

    def remboursée(self,obj):
        return hasattr(obj, 'remboursement')
    
    remboursée.boolean = remboursée

