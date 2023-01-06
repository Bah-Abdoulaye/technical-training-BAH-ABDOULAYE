class SaleReport(models.AbstractModel):
    _inherit = 'report.sale.report_saleorder'

    
    def _get_report_values(self, docids, data=None):
        report = super()._get_report_values(docids, data)
        report['lines'].mapped('order_line').write({
            'training_date': fields.Char(string="Training Date"),
            'employe_id': fields.Many2one('res.partner', string='Employe')
        })
        return report