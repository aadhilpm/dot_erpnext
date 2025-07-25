import frappe

def after_install():
	"""Setup default DOTS Integration Settings after app installation"""
	try:
		# Check if settings already exist
		if not frappe.db.exists("DOTS Integration Settings", "DOTS Integration Settings"):
			# Create default settings document
			settings = frappe.new_doc("DOTS Integration Settings")
			settings.title = "DOTS Integration Settings"
			settings.api_url = "https://site.dotshr.com/apisite/dndApi/Attendance_bydate"
			settings.sync_frequency = 15
			settings.enabled = 0
			settings.insert(ignore_permissions=True)
			
			frappe.db.commit()
			print("DOTS Integration Settings created successfully")
		
		# Setup custom fields
		setup_custom_fields()
		
	except Exception as e:
		print(f"Error setting up DOTS Integration: {str(e)}")

def setup_custom_fields():
	"""Setup custom fields for DOTS integration"""
	try:
		# Create custom project field in Employee Checkin
		if not frappe.db.exists("Custom Field", "Employee Checkin-custom_project"):
			custom_field = frappe.new_doc("Custom Field")
			custom_field.dt = "Employee Checkin"
			custom_field.fieldname = "custom_project"
			custom_field.label = "Project"
			custom_field.fieldtype = "Link"
			custom_field.options = "Project"
			custom_field.insert_after = "device_id"
			custom_field.description = "Project information from DOTS attendance system"
			custom_field.in_list_view = 1
			custom_field.in_standard_filter = 1
			custom_field.insert(ignore_permissions=True)
			
			frappe.db.commit()
			print("Custom field 'custom_project' created successfully in Employee Checkin")
		else:
			print("Custom field 'custom_project' already exists")
			
	except Exception as e:
		print(f"Error setting up custom fields: {str(e)}")