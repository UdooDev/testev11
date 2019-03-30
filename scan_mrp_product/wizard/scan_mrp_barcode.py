from odoo import api, fields, models
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class WizardMRPSerial(models.TransientModel):
	_name = 'wizard.mrp.scan.dev.serial'
	_inherit = 'barcodes.barcode_events_mixin'
	_description = 'Scan ProductSerial'
	
	
	def on_barcode_scanned(self, barcode):
		self.ensure_one()
		#search mrp
		raise UserError("Events Received " + barcode)
		if barcode:
			mrp = self.env['mrp.production'].search([('name', '=', barcode)])
			if mrp:
				action = self.env.ref('mrp.mrp_production_action').read()[0]
				action['views'] = [(self.env.ref('mrp.mrp_production_form_view').id, 'form')]
				action['res_id'] = mrp.ids[0]
			else:
				action = {'type': 'ir.actions.act_window_close'}
			_logger.info('>>>>>>>>>>>>> %s', action)
			return action