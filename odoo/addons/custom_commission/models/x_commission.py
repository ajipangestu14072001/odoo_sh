from odoo import models, fields, api

class XCommission(models.Model):
    _name = 'x.commission'
    _description = 'Sales Commission'

    name = fields.Char('Commission Name', required=True)
    percentage = fields.Float('Commission Percentage', required=True)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', required=True)
    commission_amount = fields.Float('Commission Amount', compute='_compute_commission', store=True)
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', required=True)

    @api.depends('sale_order_id.amount_total', 'percentage')
    def _compute_commission(self):
        for record in self:
            record.commission_amount = (record.sale_order_id.amount_total * record.percentage) / 100

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    commission_ids = fields.One2many('x.commission', 'sale_order_id', string='Commissions')
