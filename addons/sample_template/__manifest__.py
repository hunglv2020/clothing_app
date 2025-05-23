{
    'name': "Sample Template",
    'version': '17.0',
    'depends': ['base', 'hr', 'spreadsheet_oca', 'material_warehouse', 'base_setup', 'web'],
    'author': "Hung Le",
    'category': 'Category',
    'description': """
		    Nothing to see here, just a sample template.
    """,
    'license': 'LGPL-3',
    # data files always loaded at installation
    'data': [
        "security/sample_template_security.xml",
        "security/ir.model.access.csv",
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
            
            'sample_template/static/lib/gridjs/gridjs.umd.js',
            'sample_template/static/lib/gridjs/mermaid.min.css',

            'sample_template/static/src/components/grid_table/*.js',
            'sample_template/static/src/components/grid_table/*.xml',

        ],
    },
    'sequence': 1,
    'application': True,
}

