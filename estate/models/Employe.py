class Employe(models.Model):
    _inherit = 'res.partner'
    sale_order_line_ids = fields.One2many('sale.order.line', 'employe_id', string='Sale Order Lines')