# -*- coding: utf-8 -*-

{
	'name': 'Ex. Request Try Demo',
	'version': '1.0',
	'author': 'BUSO Co. Ltd',
	'category': 'Fresher',
	'summary': 'Ex - Request - Try - Demo',
	'website': 'https://www.busovn.com',
	'description': """

	""",
	'depends': ['sale','web','mail'],
	'data': [
		'security/ir.model.access.csv',
		'views/partner_request_view.xml',
		'data/mail_remaining_template.xml',
		'data/email_template.xml',
		'data/data.xml',
		'data/remaining_days_schedule_action.xml',		

		
	],
	'installable': True,
	'auto_install': False,
}

