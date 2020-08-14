# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime, timedelta
from dateutil import relativedelta
from datetime import date
from openerp.exceptions import UserError, ValidationError
import time
import base64
import dateutil.parser
import requests
import httplib
import json
import vio_request_data
import logging

_logger = logging.getLogger(__name__)

VIO_API_URL = "qa.api.vio.findo.com.ar"
VIO_PENDING_REQUESTS = "/apivio/v1/pendingRequests"
VIO_REQUEST_DATA = "/apivio/v1/requestData/"
VIO_PREOCESS_REQUESTS = "/apivio/v1/processRequest/"
class ExtendsResPartnerFindo(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'

	# Vio Personal
	findo_date_inform = fields.Date('Fecha del informe')
	findo_date_inform_risk = fields.Date(related='findo_date_inform')
	findo_name = fields.Char('Nombre')
	findo_name_risk = fields.Char(related='findo_name')
	findo_dni = fields.Char('Identificacion')
	findo_dni_risk = fields.Char(related='findo_dni')
	findo_nacimiento = fields.Date('Fecha de nacimiento')
	findo_mobile = fields.Char('Celular')
	# Vio Risk
	findo_score = fields.Integer('Score')
	findo_score_risk = fields.Integer(related='findo_score')
	# VioIncomeRank - Ingreso Declarado
	findo_declared_personal_income = fields.Integer('Ingreso declarado')
	findo_declared_personal_income_risk = fields.Integer(related='findo_declared_personal_income')
	findo_couple_income = fields.Integer('Ingreso de la pareja')
	findo_other_income = fields.Integer('Otros ingresos')
	findo_total_income = fields.Integer('Total ingresos')
	findo_total_income_risk = fields.Integer(related='findo_total_income')
	findo_housing_property = fields.Char('Propiedad de la vivienda')
	findo_housing_property_risk = fields.Char(related='findo_housing_property')
	findo_housing_age = fields.Char('Antiguedad de la vivienda')
	findo_mobility = fields.Char('Tipo de transporte')
	findo_mobility_risk = fields.Char(related='findo_mobility')
	findo_studies_level = fields.Char('Nivel de estudio')
	findo_studies_level_risk = fields.Char(related='findo_studies_level')
	findo_predicted_nse = fields.Char('NSE')
	findo_predicted_nse_risk = fields.Char(related='findo_predicted_nse')
	# VioID
	findo_documento_name = fields.Char('Nombre')
	findo_documento_dni = fields.Char('Identificacion')
	findo_documento_validId = fields.Boolean('Fecha valida y es el declarado')
	findo_documento_validRenaper = fields.Boolean('Documento valido?')
	findo_documento_deathRenaper = fields.Boolean('Fallecido?')
	# VioWorkInformation
	findo_workRelationship = fields.Char('Relacion laboral')
	findo_job = fields.Char('Trabajo')
	findo_employeer = fields.Char('Es empleador')
	findo_position = fields.Char('Puesto')
	findo_work_address = fields.Char('Direccion de trabajo')
	findo_work_phone = fields.Char('Telefono de trabajo')
	# VioAddress
	findo_street = fields.Char('Direccion')
	findo_number = fields.Char('Altura')
	findo_city = fields.Char('Ciudad')
	findo_province = fields.Char('Provincia')
	findo_zipCode = fields.Char('CP')
	findo_direccion = fields.Char('Direccion', compute='_compute_findo_direccion')
	findo_direccion_risk = fields.Char(related='findo_direccion')
	findo_phoneNumber = fields.Char('Numero fijo')
	# VioAddressRenaper
	findo_renaper_street = fields.Char('Direccion')
	findo_renaper_number = fields.Char('Altura')
	findo_renaper_city = fields.Char('Ciudad')
	findo_renaper_province = fields.Char('Provincia')
	findo_renaper_zipCode = fields.Char('CP')
	findo_renaper_floor = fields.Char('Piso')
	findo_renaper_department = fields.Char('Departamento')
	findo_renaper_direccion = fields.Char('Direccion', compute='_compute_findo_renaper_direccion')
	findo_renaper_municipality = fields.Char('Municipio')
	findo_renaper_country = fields.Char('Pais')
	# CPM y Tipo
	findo_capacidad_pago_mensual = fields.Float('Findo - CPM', digits=(16,2))
	findo_capacidad_pago_mensual_risk = fields.Float(related='findo_capacidad_pago_mensual')
	findo_partner_tipo_id = fields.Many2one('financiera.partner.tipo', 'Findo - Tipo de cliente')
	findo_partner_tipo_id_risk = fields.Many2one(related='findo_partner_tipo_id')
	# Requerimientos de perfil vio
	perfil_vio_pass = fields.Boolean('Supera requerimiento de perfil VIO', compute='_compute_perfil_vio_pass')
	vio_url_install_app = fields.Char('Url de instalacion VIO', readonly=True, related='company_id.findo_configuracion_id.vio_url_install_app')
	vio_qr_install_app = fields.Binary("QR de instalacion VIO", readonly=True, related='company_id.findo_configuracion_id.vio_qr_install_app')

	@api.model
	def _pendingRequests(self):
		conn = httplib.HTTPSConnection(VIO_API_URL)
		cr = self.env.cr
		uid = self.env.uid
		company_obj = self.pool.get('res.company')
		comapny_ids = company_obj.search(cr, uid, [])
		for _id in comapny_ids:
			company_id = company_obj.browse(cr, uid, _id)
			if len(company_id.findo_configuracion_id) > 0:
				findo_configuracion_id = company_id.findo_configuracion_id
				if findo_configuracion_id.token != False:
					headers = { 'authorization': "Basic " + findo_configuracion_id.token }
					conn.request("GET", VIO_PENDING_REQUESTS, headers=headers)
					res = conn.getresponse()
					if res.status != 200:
						solicitudes_pendientes_object = json.loads(res.read())
						for solicitud in solicitudes_pendientes_object['content']:
							solicitud_id = solicitud['id']
							conn.request("GET", VIO_REQUEST_DATA + str(solicitud_id), headers=headers)
							res = conn.getresponse()
							vio_user_data_object = json.loads(res.read())
							vio_user_data_class = vio_request_data.vio_from_dict(vio_user_data_object)
							partner_id = self.vio_update_partner(vio_user_data_class, company_id)
							date_inform = datetime.fromtimestamp(solicitud['requestDate'] / 1e3)
							partner_id.findo_date_inform = date_inform
							# Ahora hay que marcar como procesada la solicitud y notificar 
							# que hay nuevas solicitudes procesadas.
							conn.request("POST", VIO_PREOCESS_REQUESTS + str(solicitud_id), {}, headers)
							response = conn.getresponse()
							if (response.status != 200):
								_logger.error("Log Error VIO preocess requests: " + response.status)
								_logger.error("Log Error VIO preocess requests reason: " + response.reason)
					else:
						_logger.error("Log Error VIO connection: " + res.status)
						_logger.error("Log Error VIO connection reason: " + res.reason)
				else:
					_logger.error("Log Error VIO token is False")
				
	def vio_update_partner(self, vio_user, company_id):
		# buscamos si existe
		cr = self.env.cr
		uid = self.env.uid
		partner_obj = self.pool.get('res.partner')
		partner_ids = partner_obj.search(cr, uid, [
			('company_id', '=', company_id.id),
			('main_id_number', '=', str(vio_user.personal.dni))
		])
		if len(partner_ids) > 0:
			# El partner existe y suponemos que es unico
			partner_id = partner_obj.browse(cr, uid, partner_ids[0])
		else:
			# El partner no existe hay que crearlo con parametros basicos de Vio
			name = (vio_user.personal.first_name or '') + ' ' + (vio_user.personal.last_name or '')
			parner_values = {
				'name': name,
				'phone': vio_user.personal.phone_number,
				'mobile': vio_user.personal.phone_number,
				'email': vio_user.sign_in.email,
				'company_id': company_id.id,
			}
			partner_id = self.env['res.partner'].create(parner_values)
			partner_id.main_id_number = vio_user.personal.dni
		# Ahora hacemos el update
		# Marcamos con etiqueta VIO al partner
		if len(company_id.findo_configuracion_id.financiera_category_id) > 0:
			partner_id.financiera_category_id = [(4, company_id.findo_configuracion_id.financiera_category_id.id)]
		# Vio Personal
		if vio_user.personal != None:
			partner_id.findo_name = (vio_user.personal.first_name or '') + ' ' + (vio_user.personal.last_name or '')
			partner_id.findo_dni = vio_user.personal.dni
			partner_id.findo_nacimiento = vio_user.personal.birthday
			partner_id.findo_mobile = vio_user.personal.phone_number
		# # Vio Risk
		if vio_user.risk != None:
			partner_id.findo_score = vio_user.risk.findo_score
			# CPM y Tipo
			partner_id.set_findo_score(vio_user.risk.findo_score)
			# # VioIncomeRank - Ingreso Declarado
			if vio_user.risk.income_rank != None:
				partner_id.findo_declared_personal_income = vio_user.risk.income_rank.declared_personal_income
				partner_id.findo_couple_income = vio_user.risk.income_rank.couple_income
				partner_id.findo_other_income = vio_user.risk.income_rank.other_income
				partner_id.findo_total_income = vio_user.risk.income_rank.total_income
				partner_id.findo_housing_property = vio_user.risk.income_rank.housing_property
				partner_id.findo_housing_age = vio_user.risk.income_rank.housing_age
				partner_id.findo_mobility = vio_user.risk.income_rank.mobility
				partner_id.findo_studies_level = vio_user.risk.income_rank.studies_level
				partner_id.findo_predicted_nse = vio_user.risk.income_rank.predicted_nse
		# VioWorkInformation
		if vio_user.work_information != None:
			partner_id.findo_workRelationship = vio_user.work_information.work_relationship
			partner_id.findo_job = vio_user.work_information.job
			partner_id.findo_employeer = vio_user.work_information.employeer
			partner_id.findo_position = vio_user.work_information.position
			partner_id.findo_work_address = vio_user.work_information.address
			partner_id.findo_work_phone = vio_user.work_information.phone_number
		# # VioAddress
		if vio_user.address != None:
			partner_id.findo_street = vio_user.address.street
			partner_id.findo_number = vio_user.address.number
			partner_id.findo_city = vio_user.address.city
			partner_id.findo_province = vio_user.address.province
			partner_id.findo_zipCode = vio_user.address.zip_code
			partner_id.findo_phoneNumber = vio_user.address.phone_number
		# # VioID
		if vio_user.id != None :
			partner_id.findo_documento_name = (vio_user.id.first_name or '') + ' ' + (vio_user.id.last_name or '')
			partner_id.findo_documento_dni = vio_user.id.id_number
			partner_id.findo_documento_validId = vio_user.id.valid_id
			partner_id.findo_documento_validRenaper = vio_user.id.valid_renaper
			partner_id.findo_documento_deathRenaper = vio_user.id.death_renaper
			# VioAddressRenaper
			if vio_user.id.renaper_address != None:
				partner_id.findo_renaper_street = vio_user.id.renaper_address.street
				partner_id.findo_renaper_number = vio_user.id.renaper_address.number
				partner_id.findo_renaper_city = vio_user.id.renaper_address.city
				partner_id.findo_renaper_province = vio_user.id.renaper_address.province
				partner_id.findo_renaper_zipCode = vio_user.id.renaper_address.zip_code
				partner_id.findo_renaper_floor = vio_user.id.renaper_address.floor
				partner_id.findo_renaper_department = vio_user.id.renaper_address.department
				partner_id.findo_renaper_municipality = vio_user.id.renaper_address.municipality
				partner_id.findo_renaper_country = vio_user.id.renaper_address.country			
		# for media in vio_user.media:
		# 	if media.name == 'SELFIE':
		# 		data = base64.b64encode(media.url) #.replace(b'\n', b'')
		# 		data = requests.get(media.url) #.replace(b'\n', b'')
		return partner_id

	@api.one
	def set_findo_name(self, name):
		self.findo_name = name

	@api.one
	def set_findo_mobile(self, mobile):
		self.findo_mobile = mobile

	@api.one
	def set_findo_score(self, score):
		configuracion_id = self.company_id.findo_configuracion_id
		cpm = configuracion_id.get_capacidad_pago_mensual_segun_score(score)
		self.findo_capacidad_pago_mensual = cpm
		if configuracion_id.asignar_capacidad_pago_mensual:
			self.capacidad_pago_mensual = cpm
		partner_tipo_id = configuracion_id.get_cliente_tipo_segun_score(score)
		self.findo_partner_tipo_id = partner_tipo_id.id
		if configuracion_id.asignar_partner_tipo_segun_score:
			self.partner_tipo_id = partner_tipo_id.id


	@api.one
	def _compute_findo_direccion(self):
		findo_direccion = ''
		if self.findo_street:
			findo_direccion = self.findo_street+' '
		if self.findo_number:
			findo_direccion += self.findo_number+', '
		if self.findo_city:
			findo_direccion += self.findo_city+', '
		if self.findo_province:
			findo_direccion += self.findo_province+', '
		if self.findo_zipCode:
			findo_direccion += self.findo_zipCode
		self.findo_direccion = findo_direccion

	@api.one
	def _compute_findo_renaper_direccion(self):
		findo_renaper_direccion = ''
		if self.findo_renaper_street:
			findo_renaper_direccion = self.findo_renaper_street+' '
		if self.findo_renaper_number:
			findo_renaper_direccion += self.findo_renaper_number+', '
		if self.findo_renaper_city:
			findo_renaper_direccion += self.findo_renaper_city+', '
		if self.findo_renaper_province:
			findo_renaper_direccion += self.findo_renaper_province+', '
		if self.findo_renaper_zipCode:
			findo_renaper_direccion += self.findo_renaper_zipCode
		if self.findo_renaper_floor:
			findo_renaper_direccion += ', '+self.findo_renaper_floor
		if self.findo_renaper_department:
			findo_renaper_direccion += self.findo_renaper_department
		self.findo_renaper_direccion = findo_renaper_direccion


	@api.multi
	def button_asignar_identidad_findo(self):
		# Solo se asignaran datos inalterables como nombre y dni
		if self.findo_dni != False:
			self.main_id_number = self.findo_dni
		if self.findo_name != False:
			self.name = self.findo_name
		return {'type': 'ir.actions.do_nothing'}
	
	@api.multi
	def button_asignar_domicilio_findo(self):
		if self.findo_street:
			self.street = self.findo_street
			if self.findo_number:
				self.findo_street += ' '+self.findo_number
		if self.findo_city:
			self.city = self.findo_city
		if self.findo_province:
			state_obj = self.pool.get('res.country.state')
			state_ids = state_obj.search(self.env.cr, self.env.uid, [
				('name', '=ilike', self.findo_province)
			])
			if len(state_ids) > 0:
				self.state_id = state_ids[0]
				country_id = state_obj.browse(self.env.cr, self.env.uid, state_ids[0]).country_id
				self.country_id = country_id.id
		if self.findo_zipCode:
			self.zip = self.findo_zipCode
		return {'type': 'ir.actions.do_nothing'}

	@api.multi
	def button_asignar_cpm_y_tipo_findo(self):
		self.partner_tipo_id = self.findo_partner_tipo_id.id
		self.capacidad_pago_mensual = self.findo_capacidad_pago_mensual
		return {'type': 'ir.actions.do_nothing'}

	@api.one
	def _compute_perfil_vio_pass(self):
		self.perfil_vio_pass = True
		findo_configuracion_id = self.company_id.findo_configuracion_id
		if len(findo_configuracion_id) > 0:
			if findo_configuracion_id.requiere_perfil_vio_para_solicitud:
				# Requiere perfil VIO
				if not self.findo_date_inform:
					self.perfil_vio_pass = False
				elif findo_configuracion_id.requiere_dias_nuevo_informe > 0:
					fecha_informe = datetime.strptime(self.findo_date_inform, "%Y-%m-%d")
					fecha_actual = datetime.now() #datetime.strptime(self.prestamo_id.precancelar_fecha, "%Y-%m-%d")
					diferencia = fecha_actual - fecha_informe
					dias = diferencia.days
					if dias > 0 and dias > findo_configuracion_id.requiere_dias_nuevo_informe:
						self.perfil_vio_pass = False

	@api.one
	def actualizar_vio_perfil(self):
		return True