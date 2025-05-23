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

    operation_set_id = fields.Many2one(
        'sample_template.operation_set',
        string="Operation Set (Template)",
        help="Selecting a template will create a private editable copy below.",
    )

    operation_line_ids = fields.One2many(
        'sample_template.operation_line',
        'specification_id',
        string="Operation Steps"
    )

    def action_create_finished_size(self):
        self.ensure_one()
        if self.finished_size_id:
            raise UserError(_("Finished Size already exists."))

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sample_template.finished_size',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_name': f"{self.name} - Finished Size [{uuid4().hex[:6]}]",
                'default_creator_id': self.env.user.id,
                'default_from_specification_id': self.id
            },
        }


    def action_open_finished_size(self):
        self.ensure_one()
        if not self.finished_size_id:
            raise UserError(_("Please select a Finished Size first."))
        if not self.finished_size_id.is_editable:
            raise UserError(_("Spreadsheet is locked."))
        return self.finished_size_id.open_spreadsheet()

    @api.onchange('quantity')
    def _onchange_quantity_update_usages(self):
        for line in self.material_usage_ids:
            line.quantity_used = self.quantity or 0.0


    def action_copy_operations_from_template(self):
        self.ensure_one()
        if not self.operation_set_id:
            return

        self.operation_line_ids.unlink()

        for line in self.operation_set_id.operation_line_ids:
            self.env['sample_template.operation_line'].create({
                'specification_id': self.id,
                'name': line.name,
                'sequence': line.sequence,
                'unit_price': line.unit_price,
                'quantity': line.quantity,
                'note': line.note,
            })

    def action_prepare_new_operation_set(self):
        self.ensure_one()
        if not self.operation_line_ids:
            raise UserError("No operations to save.")

        default_lines = []
        for line in self.operation_line_ids:
            default_lines.append((0, 0, {
                'name': line.name,
                'sequence': line.sequence,
                'unit_price': line.unit_price,
                'quantity': line.quantity,
                'note': line.note,
            }))

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sample_template.operation_set',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_name': f"{self.name} - Ops [{uuid4().hex[:6]}]",
                'default_note': f"Copied from specification: {self.name}",
                'default_operation_line_ids': default_lines,
            }
        }


    other_cost_line_ids = fields.One2many(
        'sample_template.other_cost_line',
        'specification_id',
        string='Other Costs'
    )

    other_cost_set_id = fields.Many2one(
        'sample_template.other_cost_set',
        string="Other Cost Set"
    )

    total_other_cost = fields.Float(
        string="Total Other Cost",
        compute="_compute_total_other_cost",
        store=True
    )

    @api.depends('other_cost_line_ids.amount')
    def _compute_total_other_cost(self):
        for rec in self:
            rec.total_other_cost = sum(line.amount for line in rec.other_cost_line_ids if line.active)

    def action_copy_other_costs_from_set(self):
        self.ensure_one()
        if not self.other_cost_set_id:
            return

        self.other_cost_line_ids.unlink()

        for line in self.other_cost_set_id.other_cost_line_ids:
            self.env['sample_template.other_cost_line'].create({
                'specification_id': self.id,
                'cost_name': line.cost_name,
                'cost_type': line.cost_type,
                'amount': line.amount,
                'invoice_date': line.invoice_date,
                'vendor_id': line.vendor_id.id,
                'ref_doc': line.ref_doc,
                'note': line.note,
                'is_estimated': line.is_estimated,
                'sequence': line.sequence,
                'state': line.state,
            })

    def action_prepare_new_other_cost_set(self):
        self.ensure_one()
        if not self.other_cost_line_ids:
            raise UserError("No Other Costs to save.")

        default_lines = []
        for line in self.other_cost_line_ids:
            default_lines.append((0, 0, {
                'cost_name': line.cost_name,
                'cost_type': line.cost_type,
                'amount': line.amount,
                'invoice_date': line.invoice_date,
                'vendor_id': line.vendor_id.id,
                'ref_doc': line.ref_doc,
                'note': line.note,
                'is_estimated': line.is_estimated,
                'sequence': line.sequence,
                'state': line.state,
            }))

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sample_template.other_cost_set',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_name': f"{self.name} - Cost Set",
                'default_note': f"Saved from: {self.name}",
                'default_other_cost_line_ids': default_lines,  # rất quan trọng
            }
        }


    process_requirement_set_id = fields.Many2one(
        'sample_template.process_requirement_set',
        string="Process Requirement Set"
    )

    process_requirements = fields.Html(string="Process Requirements")

    def action_copy_process_requirements_from_set(self):
        self.ensure_one()
        if self.process_requirement_set_id:
            self.process_requirements = self.process_requirement_set_id.content

    def action_prepare_new_process_requirement_set(self):
        self.ensure_one()
        if not self.process_requirements:
            raise UserError("No content to save.")
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sample_template.process_requirement_set',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_name': f"{self.name} - Process [{uuid4().hex[:6]}]",
                'default_note': f"Saved from: {self.name}",
                'default_content': self.process_requirements
            }
        }
    
    spec_image_ids = fields.One2many(
        'sample_template.spec_image',
        'specification_id',
        string="Images"
    )
