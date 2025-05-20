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
        'views/operation_set_views.xml',

        "views/sample_template_action.xml",
        "views/sample_template_menu.xml",

    ],
    # data files containing optionally loaded demonstration data
    'demo': [

    ],
    'sequence': 1,
    'application': True,
}

