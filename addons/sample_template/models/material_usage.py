from odoo import models, fields, api

class MaterialUsage(models.Model):
    _name = 'sample_template.material_usage'
    _description = 'Material Usage for Sample Specification'

    specification_id = fields.Many2one('sample_template.specification', required=True, ondelete='cascade')
    material_id = fields.Many2one('material_warehouse.material', required=True)

    material_name = fields.Char(string="Material Name")
    material_type = fields.Selection([
        ('fabric', 'Fabric'),
        ('label', 'Label'),
        ('button', 'Button'),
        ('accessory', 'Accessory'),
        ('other', 'Other'),
    ], string="Material Type")
    color = fields.Char()
    color_code = fields.Char()
    specification = fields.Char()
    unit = fields.Selection([
        ('m', 'Meter'),
        ('kg', 'Kilogram'),
        ('pcs', 'Pieces'),
        ('roll', 'Roll'),
        ('bag', 'Bag'),
    ])
    default_price = fields.Float()
    supplier = fields.Char()
    note = fields.Text()
    quantity_used = fields.Float()
    quantity_in_stock = fields.Float(readonly=True)
    total_cost = fields.Float(string="Total Cost", compute="_compute_total_cost", store=True)


    @api.onchange('material_id')
    def _onchange_material_id_fill_fields(self):
        m = self.material_id
        if m:
            self.material_name = m.name
            self.material_type = m.material_type
            self.color = m.color
            self.color_code = m.color_code
            self.specification = m.specification
            self.unit = m.unit
            self.default_price = m.default_price
            self.supplier = m.supplier
            self.note = m.note

            stock = self.env['material_warehouse.stock'].search([
                ('material_id', '=', m.id),
                # ('location', 'ilike', 'Main Warehouse')
            ], limit=1)
            self.quantity_in_stock = stock.quantity if stock else 0.0

            if self.specification_id and self.specification_id.quantity:
                self.quantity_used = self.specification_id.quantity

    @api.depends('default_price', 'quantity_used')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = rec.default_price * rec.quantity_used if rec.default_price and rec.quantity_used else 0.0

