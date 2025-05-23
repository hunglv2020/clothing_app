from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import json
import logging

_logger = logging.getLogger(__name__)

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

        spec_id = self.env.context.get('default_from_specification_id')
        if spec_id:
            spec = self.env['sample_template.specification'].browse(spec_id)
            spec.finished_size_id = record.id

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

    spreadsheet_data_processed = fields.Json(
        string="Processed Spreadsheet Matrix",
        compute="_compute_spreadsheet_data_processed",
        store=True,
        readonly=False,
    )

    @api.depends('spreadsheet_binary_data')
    def _compute_spreadsheet_data_processed(self):
        for rec in self:
            try:
                matrix = rec._parse_spreadsheet_to_matrix()
                rec.spreadsheet_data_processed = matrix
                _logger.info(f"[DEBUG] FinishedSize {rec.name}: computed matrix = {json.dumps(matrix)}")
            except Exception as e:
                _logger.warning(f"[WARN] Cannot compute spreadsheet matrix for {rec.name}: {e}")
                rec.spreadsheet_data_processed = []

    def _parse_spreadsheet_to_matrix(self):
        """Parse spreadsheet_binary_data (base64-encoded JSON) into a 2D matrix of values"""
        if not self.spreadsheet_binary_data:
            return []

        # Decode base64 and parse JSON
        try:
            raw_json_str = base64.b64decode(self.spreadsheet_binary_data).decode('utf-8')
            raw = json.loads(raw_json_str)
        except Exception as e:
            _logger.warning(f"[WARN] Failed to decode spreadsheet: {e}")
            return []

        sheets = raw.get('sheets', [])
        if not sheets:
            return []

        cells = sheets[0].get('cells', {})
        if not cells:
            return []

        # --- Tìm max row và max col ---
        import re

        def col_letter_to_index(col_letter):
            result = 0
            for c in col_letter:
                result = result * 26 + (ord(c.upper()) - ord('A') + 1)
            return result

        max_row = 0
        max_col_index = 0

        for cell_key in cells:
            match = re.match(r"([A-Z]+)(\d+)", cell_key)
            if match:
                col_letters, row_str = match.groups()
                row = int(row_str)
                col_index = col_letter_to_index(col_letters)

                max_row = max(max_row, row)
                max_col_index = max(max_col_index, col_index)

        # --- Dựng matrix từ A1 tới max_col và max_row ---
        matrix = []
        for row_index in range(1, max_row + 1):
            row_data = []
            for col_index in range(1, max_col_index + 1):
                # Convert col_index back to letter(s)
                col = ""
                idx = col_index
                while idx > 0:
                    idx, rem = divmod(idx - 1, 26)
                    col = chr(65 + rem) + col

                cell_key = f"{col}{row_index}"
                cell = cells.get(cell_key, {})
                value = cell.get('content', '')
                row_data.append(value)
            matrix.append(row_data)

        return matrix