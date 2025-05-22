from odoo import models, fields, api

class ProcessRequirementSet(models.Model):
    _name = 'sample_template.process_requirement_set'
    _description = 'Reusable Process Requirement Set'
    _rec_name = 'name'

    name = fields.Char(string="Set Name", required=True)
    note = fields.Text(string="Description")
    content = fields.Html(string="Requirement Content")