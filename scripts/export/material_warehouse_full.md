# Structure of `material_warehouse`

```
material_warehouse/
├── __init__.py
├── __manifest__.py
├── data
│   └── material_and_stock_demo.xml
├── models
│   ├── __init__.py
│   ├── material.py
│   └── stock.py
└── views
    ├── material_view.xml
    ├── material_warehouse_action.xml
    ├── material_warehouse_menu.xml
    └── stock_view.xml
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
    'name': "Material Warehouse",
    'version': '17.0',
    'depends': ['base', 'base_setup'],
    'author': "Hung Le",
    'category': 'Category',
    'description': """
		    Nothing to see here, just a sample template.
    """,
    'license': 'LGPL-3',
    # data files always loaded at installation
    'data': [
        'views/material_view.xml',
        'views/stock_view.xml',
        'views/material_warehouse_action.xml',
        'views/material_warehouse_menu.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        "data/material_and_stock_demo.xml",
    ],
    'sequence': 1,
    'application': True,
}
```

## `data/material_and_stock_demo.xml`

```xml
<odoo>
  <record id="material_mat_cotton_fabric_white" model="material_warehouse.material">
    <field name="name">Cotton Fabric White</field>
    <field name="material_type">fabric</field>
    <field name="color">White</field>
    <field name="color_code">W01</field>
    <field name="specification">Cotton 100%, 40s</field>
    <field name="unit">m</field>
    <field name="default_price">25000</field>
    <field name="supplier">ABC Textile Co.</field>
    <field name="note">Soft and breathable</field>
    <field name="active">1</field>
  </record>

  <record id="material_mat_button_black" model="material_warehouse.material">
    <field name="name">Button - Plastic Black</field>
    <field name="material_type">button</field>
    <field name="color">Black</field>
    <field name="color_code">B02</field>
    <field name="specification">Plastic, 4-hole</field>
    <field name="unit">pcs</field>
    <field name="default_price">200</field>
    <field name="supplier">ButtonWorld Ltd.</field>
    <field name="active">1</field>
  </record>

  <record id="material_mat_care_label" model="material_warehouse.material">
    <field name="name">Care Label</field>
    <field name="material_type">label</field>
    <field name="color">White</field>
    <field name="color_code">W02</field>
    <field name="specification">Printed Nylon</field>
    <field name="unit">pcs</field>
    <field name="default_price">100</field>
    <field name="supplier">LabelPro Co.</field>
    <field name="note">Wash instructions in EN/VN</field>
    <field name="active">1</field>
  </record>

  <record id="stock_mat_cotton_fabric_white" model="material_warehouse.stock">
    <field name="material_id" ref="material_mat_cotton_fabric_white"/>
    <field name="quantity">120</field>
    <field name="location">Main Warehouse</field>
  </record>

  <record id="stock_mat_button_black" model="material_warehouse.stock">
    <field name="material_id" ref="material_mat_button_black"/>
    <field name="quantity">5000</field>
    <field name="location">Button Shelf</field>
  </record>

  <record id="stock_mat_care_label" model="material_warehouse.stock">
    <field name="material_id" ref="material_mat_care_label"/>
    <field name="quantity">2000</field>
    <field name="location">Label Rack</field>
  </record>
</odoo>
```

## `models/__init__.py`

```python
from . import material
from . import stock
```

## `models/material.py`

```python
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
```

## `models/stock.py`

```python
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
```

## `views/material_warehouse_menu.xml`

```xml
<odoo>
  <data>
    <!-- Root menu -->
    <menuitem id="menu_material_warehouse_root" name="Material Warehouse" sequence="10"/>

    <!-- Sub-menus -->
    <menuitem id="menu_material_list" name="Materials"
              parent="menu_material_warehouse_root"
              action="action_material_list"/>

    <menuitem id="menu_stock_list" name="Stock"
              parent="menu_material_warehouse_root"
              action="action_material_stock"/>
  </data>
</odoo>
```

## `views/material_warehouse_action.xml`

```xml
<odoo>
    <record id="action_material_list" model="ir.actions.act_window">
        <field name="name">Materials</field>
        <field name="res_model">material_warehouse.material</field>
        <field name="view_mode">tree,form</field>
    </record>

    <record id="action_material_stock" model="ir.actions.act_window">
        <field name="name">Material Stock</field>
        <field name="res_model">material_warehouse.stock</field>
        <field name="view_mode">tree,form</field>
    </record>
</odoo>
```

## `views/stock_view.xml`

```xml
<odoo>
    <!-- Tree View: Stock List -->
    <record id="view_material_warehouse_stock_tree" model="ir.ui.view">
        <field name="name">material_warehouse.stock.tree</field>
        <field name="model">material_warehouse.stock</field>
        <field name="arch" type="xml">
            <tree string="Stock Quantities">
                <field name="material_id"/>
                <field name="quantity"/>
                <field name="location"/>
            </tree>
        </field>
    </record>

    <!-- Form View: Stock Detail -->
    <record id="view_material_warehouse_stock_form" model="ir.ui.view">
        <field name="name">material_warehouse.stock.form</field>
        <field name="model">material_warehouse.stock</field>
        <field name="arch" type="xml">
            <form string="Material Stock">
                <sheet>
                    <separator string="Stock Information"/>
                    <group col="3">
                        <group>
                            <field name="material_id"/>
                            <field name="location"/>
                        </group>
                        <group>
                            <field name="quantity"/>
                        </group>
                    </group>
                </sheet>
            </form>
        </field>
    </record>
</odoo>
```

## `views/material_view.xml`

```xml
<odoo>
    <!-- Tree View: Material List -->
    <record id="view_material_warehouse_material_tree" model="ir.ui.view">
        <field name="name">material_warehouse.material.tree</field>
        <field name="model">material_warehouse.material</field>
        <field name="arch" type="xml">
            <tree string="Materials">
                <field name="name"/>
                <field name="material_type"/>
                <field name="color"/>
                <field name="color_code"/>
                <field name="specification"/>
                <field name="unit"/>
                <field name="default_price"/>
                <field name="supplier"/>
                <field name="active"/>
            </tree>
        </field>
    </record>

    <!-- Form View: Material Detail -->
    <record id="view_material_warehouse_material_form" model="ir.ui.view">
        <field name="name">material_warehouse.material.form</field>
        <field name="model">material_warehouse.material</field>
        <field name="arch" type="xml">
            <form string="Material">
                <sheet>
                    <separator string="Basic Information"/>
                    <group col="3">
                        <group>
                            <field name="name"/>
                            <field name="material_type"/>
                            <field name="unit"/>
                            <field name="active"/>
                        </group>
                        <group>
                            <field name="color"/>
                            <field name="color_code"/>
                            <field name="specification"/>
                        </group>
                        <group>
                            <field name="default_price"/>
                            <field name="supplier"/>
                            <field name="note"/>
                        </group>
                    </group>
                </sheet>
            </form>
        </field>
    </record>
</odoo>
```

