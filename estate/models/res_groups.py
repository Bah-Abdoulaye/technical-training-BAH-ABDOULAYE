from odoo import fields, models

class ResGroups(models.Model):
    _inherit = 'res.groups'
    max_amount = fields.Float(string="Training max price approval")
    #permet de stocker le montant d'approbation max
    approval_amount = fields.Float(string="Approval Amount")
    #permet de stocker le niveau d'approbation associé à chaque groupe (1 => manager 1 ,2 => manager 2...)
    approval_level = fields.Integer(string="Approval Level")
