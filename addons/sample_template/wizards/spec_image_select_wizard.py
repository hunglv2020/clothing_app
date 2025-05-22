from odoo import models, fields, api

class SpecImageSelectWizard(models.TransientModel):
    _name = 'spec.image.select.wizard'
    _description = 'Select Specification Images'

    specification_id = fields.Many2one('sample_template.specification', required=True)
    image_ids = fields.Many2many('sample_template.spec_image', string="Available Images")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if 'specification_id' in self.env.context:
            spec = self.env['sample_template.specification'].browse(self.env.context['specification_id'])
            res['specification_id'] = spec.id
        return res

    def action_assign_images(self):
        for wizard in self:
            for img in wizard.image_ids:
                img.specification_id = wizard.specification_id.id
