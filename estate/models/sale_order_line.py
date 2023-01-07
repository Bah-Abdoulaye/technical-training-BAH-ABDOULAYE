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


    def _compute_approval_level_required(self):
        for order in self:
            total_amount = sum(line.price_subtotal for line in order.order_line)
            for group in self.env['res.groups'].search([], order='approval_amount desc'):
                if total_amount <= group.approval_amount:
                    order.approval_level_required = group.approval_level
                    break

#vérifie si l'utilisateur connecté a le niveau d'approbation requis pour approuver la commande
    def approve_order(self):
        user = self.env.user
        if not user.has_group('sales_team.group_sale_manager'):
            raise UserError(_("You must be a sales manager to approve orders."))
        if user.approval_level < self.approval_level_required:
            raise UserError(_("You don't have the required approval level to approve this order."))
        self.approval_state = 'approved'
        self.add_event_to_calendar()