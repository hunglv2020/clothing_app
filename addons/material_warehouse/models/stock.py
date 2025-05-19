from odoo import models, fields

class Stock(models.Model):
    _name = 'material_warehouse.stock'
    _description = 'Material Stock'
    _rec_name = 'material_id'

    material_id = fields.Many2one('material_warehouse.material', string="Material", required=True, ondelete='cascade')
    quantity = fields.Float(string="Quantity in Stock", default=0.0)
    location = fields.Char(string="Storage Location", default="Main Warehouse")

    _sql_constraints = [
        ('unique_material_location',
         'unique(material_id, location)',
         'Only one stock record per material and location is allowed.')
    ]