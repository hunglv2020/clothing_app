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

