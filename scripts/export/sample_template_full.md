# Structure of `sample_template`

```
sample_template/
├── __init__.py
├── __manifest__.py
├── models
│   ├── __init__.py
│   ├── finished_size.py
│   ├── material_usage.py
│   ├── operation_line.py
│   ├── operation_set.py
│   ├── other_cost_line.py
│   ├── other_cost_set.py
│   ├── process_requirement_set.py
│   ├── spec_image.py
│   └── specification.py
├── static
│   └── src
│       └── scss
│           └── custom.scss
└── views
    ├── finished_size_view.xml
    ├── operation_set_view.xml
    ├── other_cost_set_view.xml
    ├── process_requirement_set_view.xml
    ├── sample_template_action.xml
    ├── sample_template_menu.xml
    ├── spec_image_view.xml
    └── specification_view.xml
```

---

# File Contents

## `__init__.py`

```python
from . import models
```

## `__manifest__.py`

```python
{
    'name': "Sample Template",
    'version': '17.0',
    'depends': ['base', 'hr', 'spreadsheet_oca', 'material_warehouse'],
    'author': "Hung Le",
    'category': 'Category',
    'description': """
		    Nothing to see here, just a sample template.
    """,
    'license': 'LGPL-3',
    # data files always loaded at installation
    'data': [
        "views/specification_view.xml",
        "views/finished_size_view.xml",
        'views/operation_set_view.xml',
        'views/other_cost_set_view.xml',
        'views/process_requirement_set_view.xml',
        'views/spec_image_view.xml',

        "views/sample_template_action.xml",
        "views/sample_template_menu.xml",

    ],
    # data files containing optionally loaded demonstration data
    'demo': [

    ],
    'assets': {
        'web.assets_backend': [
            "sample_template/static/src/scss/custom.scss",
        ],
    },
    'sequence': 1,
    'application': True,
}
```

## `static/src/scss/custom.scss`

```text
/* ==== Editor Style ==== */
.o_field_html.big-editor .note-editable {
    min-height: 300px !important;
}

/* ==== Kanban View Styling for SpecImage ==== */
.o_spec_image_kanban .o_spec_image_card {
    width: 260px;
    border-radius: 8px;
    background-color: white;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
    transition: transform 0.15s ease-in-out;
}
.o_spec_image_kanban .o_spec_image_card:hover {
    transform: translateY(-2px);
}

.o_spec_image_kanban .o_spec_image_container {
    height: 180px;
    background: #f5f5f5;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}

.o_spec_image_kanban .o_spec_image_large img {
    width: 100% !important;
    height: 100% !important;
    object-fit: contain !important;
}

.o_spec_image_preview img {
    max-width: 100% !important;
    max-height: 600px !important;
    object-fit: contain !important;
}

/* ==== Kanban Horizontal Wrap Layout ==== */
.horizontal-kanban.o_kanban_view .o_kanban_renderer {
    display: flex !important;
    flex-wrap: wrap !important;
    gap: 12px;
    padding: 10px;
}

.horizontal-kanban .o_kanban_record {
    width: 260px;
    display: block !important;
}
```

## `models/__init__.py`

```python
from . import specification
from . import finished_size
from . import material_usage
from . import operation_set
from . import operation_line
from . import other_cost_set
from . import other_cost_line
from . import process_requirement_set
from . import spec_image
```

## `models/process_requirement_set.py`

```python
from odoo import models, fields, api

class ProcessRequirementSet(models.Model):
    _name = 'sample_template.process_requirement_set'
    _description = 'Reusable Process Requirement Set'
    _rec_name = 'name'

    name = fields.Char(string="Set Name", required=True)
    note = fields.Text(string="Description")
    content = fields.Html(string="Requirement Content")
```

## `models/material_usage.py`

```python
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
```

## `models/operation_line.py`

```python
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
```

## `models/operation_set.py`

```python
from odoo import models, fields

class OperationSet(models.Model):
    _name = 'sample_template.operation_set'
    _description = 'Reusable Operation Set'
    _rec_name = 'name'

    name = fields.Char(string="Set Name", required=True)
    note = fields.Text(string="Description")
    
    operation_line_ids = fields.One2many(
        'sample_template.operation_line',
        'operation_set_id',
        string="Operation Lines"
    )
```

## `models/spec_image.py`

```python
# models/spec_image.py
from odoo import models, fields

class SpecImage(models.Model):
    _name = 'sample_template.spec_image'
    _description = 'Specification Image'
    _order = 'sequence'

    name = fields.Char(string="Title / Label")
    image = fields.Binary(string="Image", store=True)
    note = fields.Text(string="Description")
    specification_id = fields.Many2one(
        'sample_template.specification',
        string="Specification",
        ondelete="set null"
    )
    sequence = fields.Integer(default=10)

    def action_unlink_self_from_specification(self):
        for record in self:
            record.specification_id = False
```

## `models/other_cost_set.py`

```python
from odoo import models, fields

class OtherCostSet(models.Model):
    _name = 'sample_template.other_cost_set'
    _description = 'Reusable Other Cost Set'
    _rec_name = 'name'

    name = fields.Char(string="Set Name", required=True)
    note = fields.Text(string="Description")

    other_cost_line_ids = fields.One2many(
        'sample_template.other_cost_line',
        'set_id',
        string="Other Cost Lines"
    )
```

## `models/specification.py`

```python
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
```

## `models/finished_size.py`

```python
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
```

## `models/other_cost_line.py`

```python
from odoo import models, fields

class OtherCostLine(models.Model):
    _name = 'sample_template.other_cost_line'
    _description = 'Other Cost Line'
    _order = 'sequence'

    specification_id = fields.Many2one('sample_template.specification', ondelete='cascade')
    set_id = fields.Many2one('sample_template.other_cost_set', ondelete='cascade')

    cost_name = fields.Char(string="Cost Name", required=True)
    cost_type = fields.Selection([
        ('rent', 'Rent'),
        ('transport', 'Transport'),
        ('utility', 'Utility'),
        ('waste', 'Waste/Loss'),
        ('other', 'Other'),
    ], string="Cost Type", default="other")

    amount = fields.Float(string="Amount", required=True)
    invoice_date = fields.Date(string="Date Incurred")
    vendor_id = fields.Many2one('res.partner', string="Vendor/Supplier")
    ref_doc = fields.Char(string="Reference Document")
    attached_file = fields.Binary(string="Attachment")
    note = fields.Char(string="Note")
    is_estimated = fields.Boolean(string="Estimated?", default=False)
    sequence = fields.Integer(string="Sequence", default=10)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], string="State", default='draft')
    active = fields.Boolean(default=True)
```

## `views/process_requirement_set_view.xml`

```xml
<odoo>
    <record id="view_process_requirement_set_tree" model="ir.ui.view">
        <field name="name">sample_template.process_requirement_set.tree</field>
        <field name="model">sample_template.process_requirement_set</field>
        <field name="arch" type="xml">
            <tree string="Process Requirement Sets">
                <field name="name"/>
                <field name="note"/>
            </tree>
        </field>
    </record>

    <record id="view_process_requirement_set_form" model="ir.ui.view">
        <field name="name">sample_template.process_requirement_set.form</field>
        <field name="model">sample_template.process_requirement_set</field>
        <field name="arch" type="xml">
            <form string="Process Requirement Set">
                <sheet>
                    <group>
                        <field name="name"/>
                        <field name="note"/>
                    </group>
                    <separator string="Requirement Content"/>
                    <field name="content" widget="html" colspan="4" class="big-editor"/>
                </sheet>
            </form>
        </field>
    </record>
</odoo>
```

## `views/spec_image_view.xml`

```xml
<odoo>
    <!-- Tree View -->
    <record id="view_spec_image_tree" model="ir.ui.view">
        <field name="name">sample_template.spec_image.tree</field>
        <field name="model">sample_template.spec_image</field>
        <field name="arch" type="xml">
            <tree>
                <field name="sequence"/>
                <field name="name"/>
                <field name="specification_id"/>
                <field name="image" widget="image"/>
                <field name="note"/>
            </tree>
        </field>
    </record>

    <!-- Form View -->
    <record id="view_spec_image_form" model="ir.ui.view">
        <field name="name">sample_template.spec_image.form</field>
        <field name="model">sample_template.spec_image</field>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <group>
                        <field name="name"/>
                        <field name="specification_id"/>
                    </group>
                    <group>
                        <field name="image" widget="image" class="o_spec_image_preview"/>
                        <field name="note"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <!-- Kanban View -->
    <record id="view_spec_image_kanban" model="ir.ui.view">
        <field name="name">sample_template.spec_image.kanban</field>
        <field name="model">sample_template.spec_image</field>
        <field name="arch" type="xml">
            <kanban class="o_spec_image_kanban" sample="1">
                <field name="name"/>
                <field name="note"/>
                <field name="image"/>
                <field name="specification_id"/>

                <templates>
                    <t t-name="kanban-box">
                        <div class="oe_kanban_global_click o_kanban_record_box o_spec_image_card shadow-sm">
                            <div class="o_spec_image_container">
                                <field name="image" widget="image" class="o_spec_image_large" options="{'zoom': true}"/>
                            </div>
                            <div class="px-2 pt-2 pb-1">
                                <div class="o_kanban_record_title fw-bold text-truncate">
                                    <field name="name" placeholder="Untitled"/>
                                </div>
                                <div class="text-muted small o_text_overflow">
                                    <field name="note"/>
                                </div>
                                <div class="text-end small text-muted" t-if="record.specification_id.raw_value">
                                    <i class="fa fa-link me-1"/><t t-esc="record.specification_id.value"/>
                                </div>
                            </div>
                        </div>
                    </t>
                </templates>
            </kanban>
        </field>
    </record>

</odoo>
```

## `views/operation_set_view.xml`

```xml
<odoo>

    <record id="view_operation_set_tree" model="ir.ui.view">
        <field name="name">operation.set.tree</field>
        <field name="model">sample_template.operation_set</field>
        <field name="arch" type="xml">
        <tree string="Operation Sets">
            <field name="name"/>
            <field name="note"/>
        </tree>
        </field>
    </record>

    <record id="view_operation_set_form" model="ir.ui.view">
        <field name="name">operation.set.form</field>
        <field name="model">sample_template.operation_set</field>
        <field name="arch" type="xml">
        <form string="Operation Set">
            <sheet>
            <group>
                <field name="name"/>
                <field name="note"/>
            </group>
            <separator string="Operation Lines"/>
            <field name="operation_line_ids">
                <tree editable="bottom">
                <field name="name"/>
                <field name="unit_price"/>
                <field name="quantity"/>
                <field name="note"/>
                <field name="total" readonly="1"/>
                </tree>
            </field>
            </sheet>
        </form>
        </field>
    </record>
</odoo>
```

## `views/sample_template_action.xml`

```xml
<odoo>

    <record id="action_specification" model="ir.actions.act_window">
        <field name="name">Sample Specifications</field>
        <field name="res_model">sample_template.specification</field>
        <field name="view_mode">tree,form</field>
    </record>

    <record id="action_finished_size" model="ir.actions.act_window">
        <field name="name">Finised Size</field>
        <field name="res_model">sample_template.finished_size</field>
        <field name="view_mode">tree,form</field>
    </record>

    <record id="action_operation_set" model="ir.actions.act_window">
        <field name="name">Operation Sets</field>
        <field name="res_model">sample_template.operation_set</field>
        <field name="view_mode">tree,form</field>
    </record>

    <record id="action_other_cost_set" model="ir.actions.act_window">
        <field name="name">Other Cost Sets</field>
        <field name="res_model">sample_template.other_cost_set</field>
        <field name="view_mode">tree,form</field>
    </record>
	
    <record id="action_process_requirement_set" model="ir.actions.act_window">
        <field name="name">Process Requirement Sets</field>
        <field name="res_model">sample_template.process_requirement_set</field>
        <field name="view_mode">tree,form</field>
    </record>

    <record id="action_spec_image" model="ir.actions.act_window">
        <field name="name">Specification Images</field>
        <field name="res_model">sample_template.spec_image</field>
        <field name="view_mode">kanban,tree,form</field>
    </record>

</odoo>
```

## `views/sample_template_menu.xml`

```xml
<odoo>
    <data>

        <menuitem id="menu_sample_template_root" name="Sample Templates" action="action_specification" sequence="10"/>

        <menuitem id="menu_specification" name="Specifications" parent="menu_sample_template_root" action="action_specification"/>
        
        <menuitem id="menu_finished_size" name="Finished Size" parent="menu_specification" action="action_finished_size"/>
        <menuitem id="menu_operation_set" name="Operation Sets" parent="menu_specification" action="action_operation_set"/>
        <menuitem id="menu_other_cost_set" name="Other Cost Sets" parent="menu_specification" action="action_other_cost_set"/>
        <menuitem id="menu_process_requirement_set" name="Process Requirement Sets" parent="menu_specification" action="action_process_requirement_set" sequence="40"/>

        <menuitem id="menu_spec_image"
                name="Specification Images"
                parent="menu_specification"
                action="action_spec_image"
                sequence="50"/>


    </data>
</odoo>
```

## `views/specification_view.xml`

```xml
<odoo>
    <record id="view_sample_template_specification_tree" model="ir.ui.view">
        <field name="name">sample_template.specification.tree</field>
        <field name="model">sample_template.specification</field>
        <field name="arch" type="xml">
            <tree string="Sample Templates">
                <field name="name"/>
                <field name="reference_code"/>
                <field name="client_id"/>
                <field name="brand"/>
                <field name="quoted_price"/>
                <field name="development_date"/>
            </tree>
        </field>
    </record>

    <record id="view_sample_template_specification_form" model="ir.ui.view">
        <field name="name">sample_template.specification.form</field>
        <field name="model">sample_template.specification</field>
        <field name="arch" type="xml">
            <form string="Sample Template">
                <sheet>
                    <separator string="Basic Information"/>
                    <group col="3">
                    <group>
                        <field name="name"/>
                        <field name="client_id"/>
                        <field name="designer"/>
                        <field name="quantity"/>
                        <field name="development_date"/>
                    </group>
                    <group>
                        <field name="reference_code"/>
                        <field name="brand"/>
                        <field name="pattern_maker"/>
                        <field name="style"/>
                        <field name="department_ids" widget="many2many_tags"/>
                    </group>
                    <group>
                        <field name="color"/>
                        <field name="quoted_price" string="Quote"/>
                        <field name="sample_maker" string="Pattern Maker"/>
                        <field name="base_size" string="Pattern Size"/>
                    </group>
                    </group>
                    <separator string="Finished Size"/>
                    <div class="d-flex justify-content-between align-items-center gap-2 mb-2">
                    <field name="finished_size_id"
                            class="flex-grow-1"
                            options="{'no_create': True}"
                            placeholder="Select Finished Size..."
                            context="{'form_view_ref': 'sample_template.view_sample_template_finished_size_form'}"/>
                    <div class="d-flex flex-wrap gap-2">
                        <button name="action_open_finished_size"
                                type="object"
                                string="Edit"
                                icon="fa-pencil"
                                class="btn btn-sm btn-primary"
                                modifiers='{"invisible": [["finished_size_id", "=", False]]}'/>
                        <button name="action_create_finished_size"
                                type="object"
                                string="New"
                                icon="fa-plus"
                                class="btn btn-sm btn-secondary"
                                modifiers='{"invisible": [["finished_size_id", "!=", False]]}'/>
                    </div>
                    </div>

                    <separator string="Materials Used" class="my-3"/>
                        <field name="material_usage_ids">
                            <tree editable="bottom">
                                <field name="material_id"/>
                                <field name="material_type" optional="show"/>
                                <field name="color" optional="show"/>
                                <field name="color_code" optional="show"/>
                                <field name="specification" optional="show"/>
                                <field name="unit" optional="show"/>
                                <field name="default_price" optional="show"/>
                                <field name="supplier" optional="show"/>
                                <field name="note" optional="show"/>
                                <field name="quantity_used"/>
                                <field name="quantity_in_stock" readonly="1"/>
                                <field name="total_cost" readonly="1"/>
                            </tree>
                        </field>

                    <separator string="Operation Steps" class="my-3"/>
                        <div class="d-flex justify-content-between align-items-center gap-2 mb-2">
                            <field name="operation_set_id"
                                class="flex-grow-1"
                                options="{'no_create': True}"
                                context="{'form_view_ref': 'sample_template.view_operation_set_form'}"
                                placeholder="Select Operation Set Template..."/>
                            <div class="d-flex flex-wrap gap-2">
                                <button name="action_copy_operations_from_template"
                                        type="object"
                                        string="Copy from Template"
                                        icon="fa-copy"
                                        class="btn btn-secondary btn-sm"
                                        modifiers='{"invisible": [["operation_set_id", "=", false]]}'/>
                                <button name="action_prepare_new_operation_set"
                                        type="object"
                                        string="Save as New Operation Set"
                                        icon="fa-save"
                                        class="btn btn-primary btn-sm"/>
                            </div>
                        </div>
                        <field name="operation_line_ids">
                            <tree editable="bottom">
                                <field name="name"/>
                                <field name="unit_price"/>
                                <field name="quantity"/>
                                <field name="note"/>
                                <field name="total" readonly="1"/>
                                <button name="action_move_up" type="object" icon="fa-arrow-up"
                                        string="Up" class="btn btn-outline-secondary btn-sm"/>
                                <button name="action_move_down" type="object" icon="fa-arrow-down"
                                        string="Down" class="btn btn-outline-secondary btn-sm"/>
                            </tree>
                        </field>

                    <separator string="Other Costs" class="my-3"/>
                    <div class="d-flex justify-content-between align-items-center gap-2 mb-2">
                        <field name="other_cost_set_id"
                            class="flex-grow-1"
                            options="{'no_create': True}"
                            placeholder="Select Other Cost Set..."/>
                        <div class="d-flex flex-wrap gap-2">
                            <button name="action_copy_other_costs_from_set"
                                    type="object"
                                    string="Copy from Set"
                                    icon="fa-copy"
                                    class="btn btn-secondary btn-sm"
                                    modifiers='{"invisible": [["other_cost_set_id", "=", false]]}'/>
                            <button name="action_prepare_new_other_cost_set"
                                    type="object"
                                    string="Save as New Cost Set"
                                    icon="fa-save"
                                    class="btn btn-primary btn-sm"/>
                        </div>
                    </div>
                    <field name="other_cost_line_ids">
                        <tree editable="bottom">
                            <field name="cost_name"/>
                            <field name="cost_type"/>
                            <field name="amount"/>
                            <field name="invoice_date" optional="hide"/>
                            <field name="vendor_id" optional="hide"/>
                            <field name="ref_doc" optional="hide"/>
                            <field name="note" optional="hide"/>
                            <field name="is_estimated" widget="boolean_toggle" optional="hide"/>
                            <field name="state" optional="hide"/>
                        </tree>
                    </field>
                    <field name="total_other_cost" readonly="1" class="mt-2"/>
                                
                    <separator string="Process Requirements" class="my-3"/>
                    <div class="d-flex justify-content-between align-items-center gap-2 mb-2">
                        <field name="process_requirement_set_id" class="flex-grow-1" options="{'no_create': True}" placeholder="Select Requirement Set..."/>
                        <div class="d-flex flex-wrap gap-2">
                            <button name="action_copy_process_requirements_from_set"
                                    type="object"
                                    string="Copy from Set"
                                    icon="fa-copy"
                                    class="btn btn-secondary btn-sm"
                                    modifiers='{"invisible": [["process_requirement_set_id", "=", false]]}'/>
                            <button name="action_prepare_new_process_requirement_set"
                                    type="object"
                                    string="Save as New Set"
                                    icon="fa-save"
                                    class="btn btn-primary btn-sm"/>
                        </div>
                    </div>
                    <field name="process_requirements" widget="html" colspan="4" class="big-editor"/>

                    <separator string="Images" class="my-3"/>
                    
                    <div class="o_spec_image_container_wrap">
                        <field name="spec_image_ids" nolabel="1">
                            <kanban style="white-space: nowrap; overflow-x: auto; overflow-y: hidden; display: block;"
                                    class="o_spec_image_kanban horizontal-kanban oe_kanban_sortable"
                                    default_order="sequence"
                                    data-record-sort-field="sequence">
                                <field name="name"/>
                                <field name="image"/>
                                <field name="sequence"/>
                                <templates>
                                    <t t-name="kanban-box">
                                        <div class="o_spec_image_card shadow-sm p-1 position-relative oe_kanban_global_click" type="open">
                                            <field name="image"
                                                   widget="image"
                                                   class="o_spec_image_large"
                                                   options="{'zoom': true}"/>
                                            <div class="fw-bold mt-1">
                                                <field name="name" placeholder="Untitled"/>
                                            </div>
                                            <button type="object"
                                                    name="action_unlink_self_from_specification"
                                                    class="btn btn-sm btn-light text-danger position-absolute top-0 end-0"
                                                    title="Remove this image">
                                                <i class="fa fa-chain-broken"/>
                                            </button>
                                        </div>
                                    </t>
                                </templates>
                            </kanban>
                        </field>
                    </div>
                </sheet>
            </form>
        </field>
    </record>

</odoo>
```

## `views/other_cost_set_view.xml`

```xml
<odoo>
    <!-- Tree View: Other Cost Set -->
    <record id="view_other_cost_set_tree" model="ir.ui.view">
        <field name="name">sample_template.other_cost_set.tree</field>
        <field name="model">sample_template.other_cost_set</field>
        <field name="arch" type="xml">
            <tree string="Other Cost Sets">
                <field name="name"/>
                <field name="note"/>
            </tree>
        </field>
    </record>

    <!-- Form View: Other Cost Set -->
    <record id="view_other_cost_set_form" model="ir.ui.view">
        <field name="name">sample_template.other_cost_set.form</field>
        <field name="model">sample_template.other_cost_set</field>
        <field name="arch" type="xml">
            <form string="Other Cost Set">
                <sheet>
                    <group>
                        <field name="name"/>
                        <field name="note"/>
                    </group>
                    <separator string="Other Cost Lines"/>
                    <field name="other_cost_line_ids">
                        <tree editable="bottom">
                            <field name="cost_name"/>
                            <field name="cost_type"/>
                            <field name="amount"/>
                            <field name="invoice_date" optional="hide"/>
                            <field name="vendor_id" optional="hide"/>
                            <field name="ref_doc" optional="hide"/>
                            <field name="note" optional="hide"/>
                            <field name="is_estimated" widget="boolean_toggle" optional="hide"/>
                            <field name="state" optional="hide"/>
                        </tree>
                    </field>
                </sheet>
            </form>
        </field>
    </record>
</odoo>
```

## `views/finished_size_view.xml`

```xml
<odoo>

    <record id="view_sample_template_finished_size_form" model="ir.ui.view">
        <field name="name">sample_template.finished_size.form</field>
        <field name="model">sample_template.finished_size</field>
        <field name="arch" type="xml">
        <form string="Finished Size Spreadsheet">
            <header>

            <button name="action_open_if_editable"
                    string="Edit Spreadsheet"
                    type="object"
                    icon="fa-pencil"
                    modifiers='{"invisible": [["is_editable", "=", False]]}'/>
            </header>
            <sheet>
            <group>
                <field name="name"/>
                <field name="creator_id" readonly="1"/>
                <field name="is_editable"/>
            </group>

            <group string="Spreadsheet Access" groups="base.group_no_one">
                <field name="contributor_ids" widget="many2many_tags"/>
                <field name="contributor_group_ids" widget="many2many_tags"/>
                <field name="reader_ids" widget="many2many_tags"/>
                <field name="reader_group_ids" widget="many2many_tags"/>
            </group>

            <group string="Technical (Hidden)" invisible="1">
                <field name="spreadsheet_binary_data" filename="filename"/>
                <field name="filename" invisible="1"/>
            </group>
            </sheet>
        </form>
        </field>
    </record>

    <record id="view_sample_template_finished_size_tree" model="ir.ui.view">
        <field name="name">sample_template.finished_size.tree</field>
        <field name="model">sample_template.finished_size</field>
        <field name="arch" type="xml">
        <tree>
            <field name="name"/>
            <field name="is_editable"/>
            <button name="action_open_if_editable" type="object" icon="fa-pencil"/>
        </tree>
        </field>
    </record>
    
</odoo>
```

