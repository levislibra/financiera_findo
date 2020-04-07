# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime, timedelta
from dateutil import relativedelta
from openerp.exceptions import UserError, ValidationError
import time
import math

class FinancieraFindoPerfilWizard(models.TransientModel):
	_name = 'financiera.findo.perfil.wizard'

	partner_id = fields.Many2one('res.partner', 'Cliente')
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

	@api.one
	def perfil_aplicar(self):
		self.partner_id.set_findo_name(self.findo_name)
		self.partner_id.set_findo_mobile(self.findo_mobile)
		self.partner_id.set_findo_perfil_letra(self.findo_perfil_letra)
