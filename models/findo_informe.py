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

	# Vio Personal
	findo_date_inform = fields.Date('Fecha del informe')
	findo_name = fields.Char('Nombre')
	findo_dni = fields.Char('Identificacion')
	findo_nacimiento = fields.Date('Fecha de nacimiento')
	findo_mobile = fields.Char('Celular')
	# Vio Risk
	findo_score = fields.Integer('Score')
	# VioIncomeRank - Ingreso Declarado
	findo_declaredPersonalIncome = fields.Integer('Ingreso declarado')
	findo_coupleIncome = fields.Integer('Ingreso de la pareja')
	findo_otherIncome = fields.Integer('Otros ingresos')
	findo_totalIncome = fields.Integer('Total ingresos')
	findo_housingProperty = fields.Char('Propiedad de la vivienda')
	findo_housingAge = fields.Char('Antiguedad de la vivienda')
	findo_mobility = fields.Char('Tipo de transporte')
	findo_studiesLevel = fields.Char('Nivel de estudio')
	findo_predictedNSE = fields.Char('NSE')
	# VioID
	findo_documento_name = fields.Char('Nombre')
	findo_documento_dni = fields.Char('Identificacion')
	findo_documento_validId = fields.Boolean('Doc. valido en fecha y coincide con el declarado')
	findo_documento_validRenaper = fields.Boolean('Renaper lo informo como documento valido?')
	findo_documento_deathRenaper = fields.Boolean('Renaper lo informa como fallecido?')
	# VioWorkInformation
	findo_workRelationship = fields.Char('Relacion laboral')
	findo_job = fields.Char('Trabajo')
	findo_employeer = fields.Char('Es empleador')
	findo_position = fields.Char('Puesto')
	# VioAddress
	findo_street = fields.Char('Direccion')
	findo_number = fields.Char('Altura')
	findo_city = fields.Char('Ciudad')
	findo_province = fields.Char('Provincia')
	findo_zipCode = fields.Char('CP')
	findo_direccion = fields.Char('Direccion', compute='_compute_findo_direccion')
	findo_phoneNumber = fields.Char('Numero fijo')
	# VioAddressRenaper
	findo_renaper_street = fields.Char('Direccion')
	findo_renaper_number = fields.Char('Altura')
	findo_renaper_city = fields.Char('Ciudad')
	findo_renaper_province = fields.Char('Provincia')
	findo_renaper_zipCode = fields.Char('CP')
	findo_renaper_floor = fields.Char('Piso')
	findo_renaper_departament = fields.Char('Departamento')
	findo_renaper_direccion = fields.Char('Direccion', compute='_compute_findo_renaper_direccion')
	findo_renaper_municipality = fields.Char('Municipio')
	findo_renaper_country = fields.Char('Pais')
	# CPM y Tipo
	findo_capacidad_pago_mensual = fields.Float('Findo - CPM', digits=(16,2))
	findo_partner_tipo_id = fields.Many2one('financiera.partner.tipo', 'Findo - Tipo de cliente')


	@api.one
	def set_findo_name(self, name):
		self.findo_name = name

	@api.one
	def set_findo_mobile(self, mobile):
		self.findo_mobile = mobile

	@api.one
	def set_findo_score(self, score):
		configuracion_id = self.company_id.findo_configuracion_id
		cpm = configuracion_id.get_capacidad_pago_mensual_segun_perfil(self.findo_score)
		self.findo_capacidad_pago_mensual = cpm
		if configuracion_id.asignar_capacidad_pago_mensual:
			self.capacidad_pago_mensual = cpm
		partner_tipo_id = configuracion_id.get_cliente_tipo_segun_perfil(self.findo_score)
		self.findo_partner_tipo_id = partner_tipo_id.id
		if configuracion_id.asignar_partner_tipo_segun_perfil:
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
		if self.findo_renaper_departament:
			findo_renaper_direccion += self.findo_renaper_departament
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
