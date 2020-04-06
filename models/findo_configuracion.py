# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime, timedelta
from dateutil import relativedelta
from openerp.exceptions import UserError, ValidationError
import time
import requests

class FinancieraFindoConfiguracion(models.Model):
	_name = 'financiera.findo.configuracion'

	name = fields.Char('Nombre')
	usuario = fields.Char('Usuario')
	password = fields.Char('Password')
	saldo_informes = fields.Integer('Saldo Informes')
	
	solicitar_informe_enviar_a_revision = fields.Boolean('Consultar informe al enviar a revision')
	asignar_capacidad_pago_mensual = fields.Boolean('Asignar capacidad de pago mensual automaticamente')
	asignar_partner_tipo_segun_perfil = fields.Boolean('Asignar tipo de cliente segun perfil automaticamente')
	perfil_to_cpm_ids = fields.One2many('financiera.findo.perfil.cpm', 'configuracion_id', 'Asignacion de CPM segun Perfil')
	company_id = fields.Many2one('res.company', 'Empresa', required=False, default=lambda self: self.env['res.company']._company_default_get('financiera.findo.configuracion'))
	
	def get_capacidad_pago_mensual_segun_perfil(self, perfil):
		result = 0
		for line in self.perfil_to_cpm_ids:
			if perfil == line.perfil:
				result = line.capacidad_pago_mensual
				break
		return result

	def get_cliente_tipo_segun_perfil(self, perfil):
		result = None
		for line in self.perfil_to_cpm_ids:
			if perfil == line.perfil:
				result = line.partner_tipo_id
				break
		return result

class FinancieraFindoPerfilToCPM(models.Model):
	_name = 'financiera.findo.perfil.cpm'

	configuracion_id = fields.Many2one('financiera.findo.configuracion', "Configuracion Findo")
	perfil = fields.Char('Perfil')
	capacidad_pago_mensual = fields.Float('Capcidad de pago mensual asignada', digits=(16,2))
	partner_tipo_id = fields.Many2one('financiera.partner.tipo', 'Tipo de cliente')
	company_id = fields.Many2one('res.company', 'Empresa', required=False, default=lambda self: self.env['res.company']._company_default_get('financiera.findo.perfil.cpm'))

class ExtendsResCompany(models.Model):
	_name = 'res.company'
	_inherit = 'res.company'

	findo_configuracion_id = fields.Many2one('financiera.findo.configuracion', 'Configuracion Findo')

