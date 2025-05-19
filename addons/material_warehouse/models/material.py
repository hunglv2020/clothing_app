from odoo import models, fields

class Material(models.Model):
    _name = 'material_warehouse.material'
    _description = 'Material'

    name = fields.Char(string="Material Name", required=True)

    material_type = fields.Selection([
        ('fabric', 'Fabric'),
        ('label', 'Label'),
        ('button', 'Button'),
        ('accessory', 'Accessory'),
        ('other', 'Other'),
    ], string="Material Type", required=True)

    color = fields.Char(string="Color")
    color_code = fields.Char(string="Color Code")
    specification = fields.Char(string="Specification")

    unit = fields.Selection([
        ('m', 'Meter'),
        ('kg', 'Kilogram'),
        ('pcs', 'Pieces'),
        ('roll', 'Roll'),
        ('bag', 'Bag'),
    ], string="Unit of Measure")

    default_price = fields.Float(string="Default Unit Price")
    supplier = fields.Char(string="Preferred Supplier")

    note = fields.Text(string="Note")
    active = fields.Boolean(default=True)
