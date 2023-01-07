from odoo import models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    
    def add_event_to_calendar(self):
        # Appel de la méthode action_confirm parente
        result = super().action_confirm()
        # Pour chaque ligne de commande de la commande de vente
        for line in self.order_line:
            # Si un employé a été sélectionné
            if line.employe_id:
                # Création d'un événement dans le calendrier de l'employé
                self.env['calendar.event'].create_event(
                    line.employe_id.id,
                    line.training_date,
                    'Formation',
                    'Formation prévue pour la date : %s' % line.training_date
                )
        return result

