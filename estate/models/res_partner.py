from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    approval_level = fields.Integer(string='Approval Level')
