from odoo import fields, models, Command

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    training_date = fields.Char(string="Training Date")
    employe_id = fields.Many2one('res.partner', string='Employe')
    event_id = fields.Many2one('calendar.event', string='Event')