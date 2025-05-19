from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
from uuid import uuid4

class SampleTemplateSpecification(models.Model):
    _name = 'sample_template.specification'
    _description = 'Sample Template Specification'

    name = fields.Char(string="Name", required=True)
    reference_code = fields.Char(string="Reference Code")
    client_id = fields.Many2one('res.partner', string="Client")
    brand = fields.Char(string="Brand")
    color = fields.Char(string="Color")
    style = fields.Char(string="Style")
    quoted_price = fields.Float(string="Quoted Price")
    designer = fields.Char(string="Designer")
    pattern_maker = fields.Char(string="Pattern Maker")
    sample_maker = fields.Char(string="Sample Maker")
    quantity = fields.Integer(string="Quantity")
    base_size = fields.Char(string="Base Size")
    development_date = fields.Date(string="Development Date")
    department_ids = fields.Many2many('hr.department', string="Departments")

    finished_size_id = fields.Many2one(
        'sample_template.finished_size',
        string="Finished Size Sheet",
        ondelete='set null',
    )

    material_usage_ids = fields.One2many(
        'sample_template.material_usage',
        'specification_id',
        string="Materials Used"
    )


    def action_create_finished_size(self):
        self.ensure_one()
        finished_size = self.env['sample_template.finished_size'].create({
            'name': f"{self.name} - Finished Size [{uuid4().hex[:6]}]",
        })
        self.finished_size_id = finished_size.id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sample_template.finished_size',
            'view_mode': 'form',
            'res_id': finished_size.id,
            'target': 'new',
        }

    def action_open_finished_size(self):
        self.ensure_one()
        if not self.finished_size_id:
            raise UserError(_("Please select a Finished Size first."))
        return self.finished_size_id.open_spreadsheet()

    @api.onchange('quantity')
    def _onchange_quantity_update_usages(self):
        for line in self.material_usage_ids:
            line.quantity_used = self.quantity or 0.0


