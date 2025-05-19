from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SampleTemplateFinishedSize(models.Model):
    _name = 'sample_template.finished_size'
    _inherit = 'spreadsheet.spreadsheet'
    _description = 'Sample Template Finished Size'
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    is_editable = fields.Boolean(string="Editable", default=True)
    creator_id = fields.Many2one(
        'res.users', string="Created by", default=lambda self: self.env.user, readonly=True
    )

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Finished Size name must be unique!'),
    ]

    # Override để tránh lỗi bảng Many2many
    contributor_ids = fields.Many2many(
        "res.users",
        relation="finished_size_contributor_rel",
        column1="finished_size_id",
        column2="user_id",
        string="Contributors",
    )
    contributor_group_ids = fields.Many2many(
        "res.groups",
        relation="finished_size_group_contributor_rel",
        column1="finished_size_id",
        column2="group_id",
        string="Contributor Groups",
    )
    reader_ids = fields.Many2many(
        "res.users",
        relation="finished_size_reader_rel",
        column1="finished_size_id",
        column2="user_id",
        string="Readers",
    )
    reader_group_ids = fields.Many2many(
        "res.groups",
        relation="finished_size_group_reader_rel",
        column1="finished_size_id",
        column2="group_id",
        string="Reader Groups",
    )

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if not record.spreadsheet_binary_data:
            record.spreadsheet_binary_data = record._empty_spreadsheet_data_base64()
        return record

    def action_open_if_editable(self):
        self.ensure_one()
        if not self.is_editable:
            raise UserError(_("Spreadsheet is locked."))
        return super().open_spreadsheet()

    @api.depends('name', 'creator_id', 'write_uid')
    def _compute_display_name(self):
        for rec in self:
            creator = rec.creator_id.name or "Unknown"
            editor = rec.write_uid.name or "Unknown"
            rec.display_name = f"{rec.name} (by {creator}, edited by {editor})"
