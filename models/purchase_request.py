# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import date


class PurchaseRequest(models.Model):
    _name = "purchase.request"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Purchase request"
    _rec_name = 'name'

    name = fields.Char(string='Số phiếu', readonly=True, default='New')
    creation_date = fields.Date(string='Ngày yêu cầu', default=fields.Date.today(), readonly=False)
    due_date = fields.Date(string='Ngày cần cấp')
    approved_date = fields.Date(string='Ngày phê duyệt', readonly=True)
    cost_total = fields.Float(string='Tổng chi phí', compute='compute_cost_total', readonly=True)

    requested_by = fields.Many2one('res.users', string='Người yêu cầu', required=True,
                                   default=lambda self: self.env.user)
    department_id = fields.Many2one('hr.department', string='Bộ phận', related='requested_by.department_id',
                                    required=True)
    company_id = fields.Many2one('res.company', string='Công ty', default=lambda self: self.env.user.company_id,
                                 readonly=True)

    reject_reason = fields.Many2one('purchase.reject.reason', string='Lý do từ chối duyệt')

    request_line_ids = fields.One2many('purchase.request.line', 'request_id', string='Chi tiết', required=True)

    status = fields.Selection([
        ('draft', 'Dự thảo'),
        ('pending', 'Chờ duyệt'),
        ('approve', 'Đã duyệt'),
        ('finish', 'Hoàn thành'),
        ('reject', 'Từ chối'),
        ('cancel', 'Hủy')],
        string='Trạng thái', default='draft', track_visibility='onchange'
    )

    def print_report(self):
        return self.env.ref('order_purchase.report_purchase_card').report_action(self)

    def print_export_excel(self):
        return self.env.ref('order_purchase.purchase_request_line_xlsx').report_action(self)

    def action_request_approval(self):
        for record in self:
            record.status = 'pending'

    def action_approve(self):
        for record in self:
            record.status = 'approve'
            record.approved_date = date.today()

    def action_cancel(self):
        for record in self:
            record.status = 'cancel'

    def action_back_to_draft(self):
        for record in self:
            record.status = 'draft'

    def action_done(self):
        for record in self:
            record.status = 'finish'

    @api.depends('request_line_ids')
    def compute_cost_total(self):
        for record in self:
            cost_total = 0
            for r in record.request_line_ids:
                cost_total += r.estimated_subtotal
            record.cost_total = cost_total

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('purchase.request') or _('New')
        d_to = date.today()
        name = 'PR.' + d_to.strftime('%d%m%y')
        vals['name'] = name + '.' + seq

        result = super(PurchaseRequest, self).create(vals)

        return result
