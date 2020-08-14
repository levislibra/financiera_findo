# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime, timedelta
from dateutil import relativedelta
from openerp.exceptions import UserError, ValidationError
import time
class FinancieraFindoConfiguracion(models.Model):
	_name = 'financiera.findo.configuracion'

	name = fields.Char('Nombre')
	usuario = fields.Char('Usuario')
	password = fields.Char('Password')
	token = fields.Char('Token')
	saldo_informes = fields.Integer('Saldo Informes')
	
	solicitar_informe_enviar_a_revision = fields.Boolean('Consultar informe al enviar a revision')
	asignar_capacidad_pago_mensual = fields.Boolean('Asignar capacidad de pago mensual automaticamente')
	asignar_partner_tipo_segun_score = fields.Boolean('Asignar tipo de cliente segun score automaticamente')
	score_to_cpm_ids = fields.One2many('financiera.findo.score.cpm', 'configuracion_id', 'Asignacion de CPM segun Perfil')
	financiera_category_id = fields.Many2one('res.partner.category', 'Etiqueta del Cliente')
	company_id = fields.Many2one('res.company', 'Empresa', required=False, default=lambda self: self.env['res.company']._company_default_get('financiera.findo.configuracion'))
	vio_url_install_app = fields.Char('Url de instalacion VIO')
	vio_qr_install_app = fields.Binary("QR de instalacion VIO")
	# Requerimientos para solicitud de prestamo
	requiere_perfil_vio_para_solicitud = fields.Boolean('Requiere perfil VIO para solicitar prestamo')
	requiere_dias_nuevo_informe = fields.Integer('Dias para requerir nuevo informe', default=365)

	def get_capacidad_pago_mensual_segun_score(self, score):
		result = 0
		for line in self.score_to_cpm_ids:
			if score == line.score:
				result = line.capacidad_pago_mensual
				break
		return result

	def get_cliente_tipo_segun_score(self, score):
		result = None
		for line in self.score_to_cpm_ids:
			if score == line.score:
				result = line.partner_tipo_id
				break
		return result

class FinancieraFindoScoreToCPM(models.Model):
	_name = 'financiera.findo.score.cpm'

	configuracion_id = fields.Many2one('financiera.findo.configuracion', "Configuracion Findo")
	score = fields.Integer('Score')
	capacidad_pago_mensual = fields.Float('Capcidad de pago mensual asignada', digits=(16,2))
	partner_tipo_id = fields.Many2one('financiera.partner.tipo', 'Tipo de cliente')
	company_id = fields.Many2one('res.company', 'Empresa', required=False, default=lambda self: self.env['res.company']._company_default_get('financiera.findo.perfil.cpm'))

class ExtendsResCompany(models.Model):
	_name = 'res.company'
	_inherit = 'res.company'

	findo_configuracion_id = fields.Many2one('financiera.findo.configuracion', 'Configuracion Findo')
