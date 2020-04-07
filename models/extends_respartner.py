# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime, timedelta
from dateutil import relativedelta
from datetime import date
from openerp.exceptions import UserError, ValidationError
import time
import requests

class ExtendsResPartnerFindo(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'

	findo_name = fields.Char('Findo - Nombre')
	findo_mobile = fields.Char('Findo - Celular')
	findo_perfil_letra = fields.Selection([
		('A', 'A. Perfil Excelente'),
		('B', 'B. Perfil Superior'),
		('C', 'C. Perfil Muy Bueno'),
		('D', 'D. Perfil Bueno'),
		('E', 'E. Perfil Adecuado'),
		('F', 'F. Perfil Con Limites'),
		('G', 'G. Perfil Insuficiente'),
		('H', 'H. Perfil Nulo'),
		('I', 'I. Perfil Incompleto')],
		'Findo - Perfil')
	findo_capacidad_pago_mensual = fields.Float('Findo - CPM', digits=(16,2))
	findo_partner_tipo_id = fields.Many2one('financiera.partner.tipo', 'Findo - Tipo de cliente')


	# @api.one
	# @api.onchange('findo_perfil_letra')
	# def _onchange_findo_perfil_letra(self):
	# 	configuracion_id = self.company_id.findo_configuracion_id
	# 	cpm = configuracion_id.get_capacidad_pago_mensual_segun_perfil(self.findo_perfil_letra)
	# 	self.findo_capacidad_pago_mensual = cpm
	# 	if configuracion_id.asignar_capacidad_pago_mensual:
	# 		self.capacidad_pago_mensual = cpm
	# 	partner_tipo_id = configuracion_id.get_cliente_tipo_segun_perfil(self.findo_perfil_letra)
	# 	self.findo_partner_tipo_id = partner_tipo_id.id
	# 	if configuracion_id.asignar_partner_tipo_segun_perfil:
	# 		self.partner_tipo_id = partner_tipo_id.id