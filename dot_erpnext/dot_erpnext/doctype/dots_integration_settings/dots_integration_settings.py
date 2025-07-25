import frappe
from frappe.model.document import Document

class DOTSIntegrationSettings(Document):
	def validate(self):
		if self.enabled and not self.api_token:
			frappe.throw("API Token is required when integration is enabled")
		
		if self.enabled and not self.sync_frequency:
			frappe.throw("Sync frequency is required when integration is enabled")
		
		# Validate employee mapping
		if self.enabled and self.use_employee_mapping and not self.employee_mapping:
			frappe.throw("Employee mapping is required when 'Use Employee ID Mapping' is enabled")
		
		# Validate project mapping
		if self.enabled and self.use_project_mapping and not self.project_mapping:
			frappe.throw("Project mapping is required when 'Use Project Name Mapping' is enabled")
	
	def on_update(self):
		# Sync frequency is handled by scheduler checking mechanism
		pass