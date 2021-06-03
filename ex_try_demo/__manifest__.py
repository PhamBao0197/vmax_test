# -*- coding: utf-8 -*-

{
	'name': 'Ex. Try Demo',
	'version': '1.0',
	'author': 'BUSO Co. Ltd',
	'category': 'Fresher',
	'summary': 'Ex - Try - Demo',
	'website': 'https://www.busovn.com',
	'description': """

	""",
	'depends': ['web','mail'],
	'data': [
		'security/ir.model.access.csv',
		
		'views/ex_try_demo_views.xml',
		'data/email_user_template.xml',
		'data/data.xml'

	],
	'installable': True,
	'auto_install': False,
}

