# -*- coding: utf-8 -*-
from odoo import fields, models


class RejectReason(models.Model):
    _name = "purchase.reject.reason"
    _description = "Reject reason"
    _rec_name = 'reason'

    date = fields.Date(string='Ngày', default=fields.Date.today())
    reason = fields.Text(string='Lý do', required=True)
