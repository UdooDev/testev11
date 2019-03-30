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
			
			if not all_scanned:
				raise UserError("All Product Scanned")
			elif move_line:
				if not move_line[0].barcode_scan:
					self.env['stock.move.line'].create(move_line[0]._prepare_move_line_vals(quantity=move_line[0].product_uom_qty))
					move_line[0].write({
						'barcode_scan': True,
						'state': 'assigned',
					})
				all_scanned = self.mrp_id.move_raw_ids.filtered(lambda r: r.barcode_scan == True)
				if all_scanned:
					self.mrp_id.action_assign()
			else:
				raise UserError("Product doesn't exist")
			#referesh 
			self.serial = ''
			
class StockMove(models.Model):
	_inherit='stock.move'
	
	barcode_scan = fields.Boolean(default=False)