from odoo import fields, models, Command

class Employe(models.Model):
    _inherit = 'res.partner'
    sale_order_line_ids = fields.One2many('sale.order.line', 'employe_id', string='Sale Order Lines')

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    training_date = fields.Char(string="Training Date")
    employe_id = fields.Many2one('res.partner', string='Employe')