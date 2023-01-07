from odoo import models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def add_event_to_calendar(self):
        # Appel de la méthode action_confirm parente
        result = super().action_confirm()

        user = self.env.user
        # Calcul du montant total de la commande
        total_amount = sum(line.price_subtotal for line in self.order_line)
        # Vérifie si l'utilisateur est dans un groupe avec un seuil d'approbation suffisant
        if not user.has_group('sales_team.group_manager_level_1') and total_amount >= 500:
            raise UserError(_("You don't have sufficient privileges to confirm this order with a total amount greater than 500."))
        if not user.has_group('sales_team.group_manager_level_2') and total_amount >= 2000:
            raise UserError(_("You don't have sufficient privileges to confirm this order with a total amount greater than 2000."))
        if not user.has_group('sales_team.group_manager_level_3') and total_amount >= 5000:
            raise UserError(_("You don't have sufficient privileges to confirm this order with a total amount greater than 5000."))
        # Vérifie si le partenaire a un montant maximum de commande autorisé et si la commande actuelle le dépasse
        if self.partner_id.max_amount and total_amount > self.partner_id.max_amount:
            raise UserError(_("This order exceeds the maximum allowed amount for the selected partner."))
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


    def request_approval(self):
        for order in self:
            # Calculer le montant total de la commande
            total_amount = sum(line.price_subtotal for line in order.order_line)
            # Trouver les groupes dont le seuil d'approbation est supérieur ou égal au montant total
            groups = self.env['res.groups'].search([('approval_threshold', '>=', total_amount)])
            # Trouver les utilisateurs ayant le moins d'approbations en attente dans chaque groupe
            users = []
            for group in groups:
                users += group.users.search([], order='pending_approvals ASC')
            # Sélectionner l'utilisateur ayant le moins d'approbations en attente
            user = users[0] if users else False
            if user:
                # Incrémenter le compteur des approbations en attente
                user.pending_approvals += 1
                # Envoyer un message à l'utilisateur dans le chat
                order.message_post(
                    body=_("You have a new approval request for the following sale order:<br/><br/>"
                        "Total amount: %s<br/>"
                        "Customer: %s") % (total))
