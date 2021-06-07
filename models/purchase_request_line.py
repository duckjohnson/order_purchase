# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError


class PurchaseRequestLine(models.Model):
    _name = "purchase.request.line"
    _description = "Purchase request line"
    _rec_name = "product"

    request_quantity = fields.Float(string='Số lượng yêu cầu', required=True)
    estimated_unit_price = fields.Float(string='Đơn giá dự kiến')
    estimated_subtotal = fields.Float(string='Chi phí dự kiến', compute='compute_estimated_subtotal')
    description = fields.Text(string='Mô tả')
    delivered_quantity = fields.Float(string='Số lượng đã mua', compute='compute_delivered_quantity')
    note = fields.Text(string='Ghi chú')

    product = fields.Many2one('product.product', string='Sản phẩm', required=True)
    unit_of_measure = fields.Char(string='Đơn vị tính', related='product.uom_name', readonly=False)

    request_id = fields.Many2one('purchase.request', string='Số phiếu')
    date_request = fields.Date(related='request_id.due_date', readonly=False)

    @api.depends('request_quantity', 'estimated_unit_price')
    def compute_estimated_subtotal(self):
        for record in self:
            record.estimated_subtotal = record.request_quantity * record.estimated_unit_price

    @api.constrains('request_quantity')
    def validate_time_focus(self):
        if self.request_quantity <= 0:
            raise UserError('Số lượng phải lớn hơn 0')

    def compute_delivered_quantity(self):
        for record in self:
            record.delivered_quantity = 0
            delivered_order = self.env['purchase.order.line'].search([('product_id', '=', record.product.id)])
            for r in delivered_order:
                record.delivered_quantity += r.product_qty
