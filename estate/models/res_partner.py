from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    #stocke le niveau d'approbation de chaque utilisateur
    approval_level = fields.Integer(string="Approval Level", compute='_compute_approval_level')
    max_amount = fields.Float(string="Maximum Allowed Order Amount")

    def _compute_approval_level(self):
        for partner in self:
            if partner.user_ids:
                user = partner.user_ids[0]
                for group in user.groups_id:
                    if group.approval_level:
                        partner.approval_level = group.approval_level
                        break
