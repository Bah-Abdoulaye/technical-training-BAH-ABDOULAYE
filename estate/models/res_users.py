class ResUsers(models.Model):
    _inherit = 'res.users'
    pending_approvals = fields.Integer(string='Pending Approvals', default=0)
