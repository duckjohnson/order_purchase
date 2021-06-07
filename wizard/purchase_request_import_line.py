# -*- coding: utf-8 -*-
import base64

import xlrd

from odoo import fields, models
from odoo.exceptions import UserError


class PurchaseRequestImportLine(models.TransientModel):
    _name = 'purchase.request.import.line'
    _description = 'Create Pop-up upload file'

    purchase_request_file = fields.Binary(string='Chọn file upload')

    def import_purchase_request_line_xlrd(self):
        data = base64.decodebytes(self.purchase_request_file)
        excel = xlrd.open_workbook(file_contents=data)
        sheet = excel.sheet_by_index(0)
        data = []

        for i in range(1, sheet.nrows):
            if not sheet.cell_value(i, 0):
                raise UserError('Không có mã sản phẩm')
            if sheet.cell_value(i, 2) <= 0:
                raise UserError('Số lượng phải lớn hơn 0')
        purchase_request_id = self.env['purchase.request'].browse(self._context.get('active_id'))

        for row in range(1, sheet.nrows):
            row_data = []
            for col in range(sheet.ncols):
                value = sheet.cell(row, col).value
                row_data.append(str(value))
            data.append(row_data)

        for i in range(1, sheet.nrows):
            product_id = self.env['product.product'].search(
                [('product_tmpl_id', '=', sheet.cell_value(i, 0))]).id
            for record in purchase_request_id:
                if record.request_line_ids:
                    for r in record.request_line_ids:
                        if r.unit_of_measure == sheet.cell_value(i, 1) and r.estimated_unit_price == float(
                                sheet.cell_value(i, 3)):
                            r.request_quantity += float(sheet.cell_value(i, 2))
                        else:
                            self.env['purchase.request.line'].create({
                                'product': product_id,
                                'request_id': record.id,
                                'unit_of_measure': sheet.cell_value(i, 1),
                                'request_quantity': sheet.cell_value(i, 2),
                                'estimated_unit_price': sheet.cell_value(i, 3),
                                'date_request': sheet.cell_value(i, 4),
                                'note': sheet.cell_value(i, 5),
                            })
                            self.env.cr.commit()
                else:
                    self.env['purchase.request.line'].create({
                        'product': product_id,
                        'request_id': purchase_request_id.id,
                        'unit_of_measure': sheet.cell_value(i, 1),
                        'request_quantity': sheet.cell_value(i, 2),
                        'estimated_unit_price': sheet.cell_value(i, 3),
                        'date_request': sheet.cell_value(i, 4),
                        'note': sheet.cell_value(i, 5),

                    })
                    self.env.cr.commit()
