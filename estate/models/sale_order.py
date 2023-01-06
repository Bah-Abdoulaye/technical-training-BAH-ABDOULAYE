from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            for line in order.order_line:
                if line.employee_id and line.training_date:
                    event_vals = {
                        'name': line.name,
                        'start': line.training_date,
                        'stop': line.training_date,
                        'allday': True,
                        'partner_ids': [(4, line.employee_id.id)],
                    }
                    event = self.env['calendar.event'].create(event_vals)
                    line.event_id = event.id
        return res