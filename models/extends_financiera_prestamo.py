# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime, timedelta
from dateutil import relativedelta
from openerp.exceptions import UserError, ValidationError
import time

class ExtendsFinancieraPrestamo(models.Model):
	_name = 'financiera.prestamo'
	_inherit = 'financiera.prestamo'

	# Requeimiento de la tarjeta de debito
	perfil_vio_pass = fields.Boolean('Supera requerimiento de perfil VIO')
	vio_url_install_app = fields.Char('Url de instalacion VIO', readonly=True, related='company_id.findo_configuracion_id.vio_url_install_app')
	vio_qr_install_app = fields.Binary("QR de instalacion VIO", readonly=True, related='company_id.findo_configuracion_id.vio_qr_install_app')
	
	@api.model
	def default_get(self, fields):
		rec = super(ExtendsFinancieraPrestamo, self).default_get(fields)
		# configuracion_id = self.env.user.company_id.configuracion_id
		context = dict(self._context or {})
		current_uid = context.get('uid')
		current_user = self.env['res.users'].browse(current_uid)
		if len(current_user.company_id.findo_configuracion_id) > 0:
			if current_user.user_has_groups('financiera_prestamos.user_portal'):
				partner_id = current_user.partner_id
				perfil_vio_pass = self.supera_perfil_vio(partner_id)
				rec.update({
					'perfil_vio_pass': perfil_vio_pass,
				})
		return rec

	def supera_perfil_vio(self, partner_id):
		ret = True
		findo_configuracion_id = partner_id.company_id.findo_configuracion_id
		if len(findo_configuracion_id) > 0:
			if findo_configuracion_id.requiere_perfil_vio_para_solicitud:
				# Requiere perfil VIO
				if not partner_id.findo_date_inform:
					ret = False
				elif findo_configuracion_id.requiere_dias_nuevo_informe > 0:
					fecha_informe = datetime.strptime(partner_id.findo_date_inform, "%Y-%m-%d")
					fecha_actual = datetime.now() #datetime.strptime(self.prestamo_id.precancelar_fecha, "%Y-%m-%d")
					diferencia = fecha_actual - fecha_informe
					dias = diferencia.days
					if dias > 0 and dias > findo_configuracion_id.requiere_dias_nuevo_informe:
						ret = False
		return ret

	@api.one
	def button_simular(self):
		# Controlar si requiere tarjeta
		self.supera_perfil_vio(self.partner_id)
		if not self.perfil_vio_pass:
			raise UserError("Debe completar el perfil VIO como se indica. No le llevara mas de 10 minutos.")
		super(ExtendsFinancieraPrestamo, self).button_simular()
		