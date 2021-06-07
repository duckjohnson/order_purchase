# -*- coding: utf-8 -*-
from odoo import fields, models


class PurchaseRequestReject(models.TransientModel):
    _name = 'purchase.request.reject'
    _description = 'Create Pop-up reject'

    reject_reason = fields.Many2one('purchase.reject.reason', string='Lý do từ chối duyệt')

    def change_status_purchase(self):
        purchase_request_id = self.env['purchase.request'].browse(self._context.get('active_id'))
        purchase_request_id.write({
            'status': 'reject',
            'reject_reason': self.reject_reason
        })
