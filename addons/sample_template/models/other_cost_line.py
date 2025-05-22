from odoo import models, fields

class OtherCostLine(models.Model):
    _name = 'sample_template.other_cost_line'
    _description = 'Other Cost Line'
    _order = 'sequence'

    specification_id = fields.Many2one('sample_template.specification', ondelete='cascade')
    set_id = fields.Many2one('sample_template.other_cost_set', ondelete='cascade')

    cost_name = fields.Char(string="Cost Name", required=True)
    cost_type = fields.Selection([
        ('rent', 'Rent'),
        ('transport', 'Transport'),
        ('utility', 'Utility'),
        ('waste', 'Waste/Loss'),
        ('other', 'Other'),
    ], string="Cost Type", default="other")

    amount = fields.Float(string="Amount", required=True)
    invoice_date = fields.Date(string="Date Incurred")
    vendor_id = fields.Many2one('res.partner', string="Vendor/Supplier")
    ref_doc = fields.Char(string="Reference Document")
    attached_file = fields.Binary(string="Attachment")
    note = fields.Char(string="Note")
    is_estimated = fields.Boolean(string="Estimated?", default=False)
    sequence = fields.Integer(string="Sequence", default=10)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], string="State", default='draft')
    active = fields.Boolean(default=True)