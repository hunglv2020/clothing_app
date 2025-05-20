from odoo import models, fields, api

class OperationLine(models.Model):
    _name = 'sample_template.operation_line'
    _description = 'Operation Line'
    _order = 'sequence'

    name = fields.Char(string="Operation Name", required=True)
    sequence = fields.Integer(string="Sequence")
    unit_price = fields.Float(string="Unit Price")
    quantity = fields.Float(string="Quantity", default=1)
    note = fields.Text()

    total = fields.Float(string="Total", compute="_compute_total", store=True)

    operation_set_id = fields.Many2one('sample_template.operation_set', ondelete="cascade")
    specification_id = fields.Many2one('sample_template.specification', ondelete="cascade")

    @api.depends('unit_price', 'quantity')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.unit_price * rec.quantity

    @api.model
    def create(self, vals):
        if 'sequence' not in vals or vals.get('sequence') in (False, 0, 10):
            # Xác định domain phù hợp theo context
            domain = []
            if vals.get("specification_id"):
                domain = [('specification_id', '=', vals['specification_id'])]
            elif vals.get("operation_set_id"):
                domain = [('operation_set_id', '=', vals['operation_set_id'])]

            max_seq = self.search(domain, order="sequence desc", limit=1).sequence or 0
            vals['sequence'] = max_seq + 1
        return super().create(vals)


    def action_move_up(self):
        for rec in self:
            other = self.search([
                ('specification_id', '=', rec.specification_id.id),
                ('sequence', '<', rec.sequence)
            ], order='sequence desc', limit=1)
            if other:
                rec.sequence, other.sequence = other.sequence, rec.sequence

    def action_move_down(self):
        for rec in self:
            other = self.search([
                ('specification_id', '=', rec.specification_id.id),
                ('sequence', '>', rec.sequence)
            ], order='sequence asc', limit=1)
            if other:
                rec.sequence, other.sequence = other.sequence, rec.sequence


