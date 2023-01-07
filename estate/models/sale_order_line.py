from odoo import fields, models, Command

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    training_date = fields.Datetime(string="Training Date")
    employe_id = fields.Many2one('res.partner', string='Employe')
    event_id = fields.Many2one('calendar.event', string='Event')
    approval_level_required = fields.Integer(string="Approval Level Required", compute='_compute_approval_level_required')
    #permet de suivre l'état d'approbation de chaque commande (en attente d'approbation, approuvée ou refusée).
    approval_state = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('refused', 'Refused')
    ], string="Approval State", default='pending')