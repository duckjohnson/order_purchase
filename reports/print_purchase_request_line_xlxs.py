# -*- coding: utf-8 -*-

from odoo import models


class PrintPurchaseRequestLineXLS(models.AbstractModel):
    _name = 'report.purchase.request.line.xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format_data = workbook.add_format({'font_size': 10, 'align': 'vcenter'})
        format_time = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        sheet = workbook.add_worksheet('Purchase order')
        sheet.set_column(1, 0, 20)
        sheet.set_column(1, 1, 20)
        sheet.set_column(1, 2, 23)
        sheet.set_column(1, 3, 20)
        sheet.set_column(1, 4, 20)
        sheet.set_column(1, 5, 23)
        sheet.set_column(1, 6, 20)
        sheet.set_column(1, 7, 20)
        sheet.write(0, 0, 'Mã sản phẩm', format1)
        sheet.write(0, 1, 'Đơn vị tính', format1)
        sheet.write(0, 2, 'Số lượng yêu cầu', format1)
        sheet.write(0, 3, 'Đơn giá dự kiến', format1)
        sheet.write(0, 4, 'Chi phí dự kiến', format1)
        sheet.write(0, 5, 'Số lượng đã mua', format1)
        sheet.write(0, 6, 'Ngày cần cấp', format1)
        sheet.write(0, 7, 'Ghi chú', format1)
        x = 1
        for record in lines:
            for r in record.request_line_ids:
                sheet.write(x, 0, r.product.id, format_data)
                sheet.write(x, 1, r.unit_of_measure, format_data)
                sheet.write(x, 2, r.request_quantity, format_data)
                sheet.write(x, 3, r.estimated_unit_price, format_data)
                sheet.write(x, 4, r.estimated_subtotal, format_data)
                sheet.write(x, 5, r.delivered_quantity, format_data)
                sheet.write(x, 6, r.date_request, format_time)
                sheet.write(x, 7, r.note, format_data)
                x += 1
