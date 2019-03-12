from odoo import api, fields, models
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class WizardMRPSerial(models.TransientModel):
	_name = 'wizard.mrp.scan.dev.serial'
	_description = 'Scan ProductSerial'

	serial = fields.Char(required=True, string='Barcode')
	
	@api.onchange('serial')
	def onchange_serial(self):
		#search mrp
		if self.serial:
			mrp = self.env['mrp.production'].search([('name', '=', self.serial)])
			if mrp:
				action = self.env.ref('mrp.mrp_production_action').read()[0]
				action['views'] = [(self.env.ref('mrp.mrp_production_form_view').id, 'form')]
				action['res_id'] = mrp.ids[0]
			else:
				action = {'type': 'ir.actions.act_window_close'}
			_logger.info('>>>>>>>>>>>>> %s', action)
			return action