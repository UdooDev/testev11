from odoo import api, fields, models
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class WizardProductSerial(models.TransientModel):
	_name = 'wizard.product.scan.dev.serial'
	_description = 'Scan ProductSerial'

	serial = fields.Char(required=True, string='Barcode')
	mrp_id = fields.Many2one('mrp.production')
	
	@api.onchange('serial')
	def onchange_serial(self):
		if self.serial:
			#search for serial in stock.production.lot
			product = self.env['product.product'].search([('barcode', '=', self.serial)])
			
			move_line = self.mrp_id.move_raw_ids.filtered(lambda r: r.product_id.id == product.id)
			all_scanned = self.mrp_id.move_raw_ids.filtered(lambda r: r.barcode_scan == False)
			
			
			_logger.info('>>>>>>>>>> found %s', move_line)
			_logger.info('>>>>>>>>>> all scanned %s', all_scanned)
			_logger.info('>>>>>>>>>> product %s', product)
			if not all_scanned:
				raise UserError("All Product Scanned")
			elif move_line:
				move_line[0].write({
					'reserved_availability': move_line.product_uom_qty,
					'barcode_scan': True
				})
			else:
				raise UserError("Product doesn't exist")
			#referesh 
			self.serial = ''
			
class StockMove(models.Model):
	_inherit='stock.move'
	
	barcode_scan = fields.Boolean(default=False)