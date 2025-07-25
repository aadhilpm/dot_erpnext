import frappe
import requests
from datetime import datetime, timedelta
from frappe.utils import getdate, now_datetime, get_datetime
import json

@frappe.whitelist()
def sync_dots_attendance(date=None):
	"""Sync attendance data from DOTS API for a specific date"""
	try:
		settings = frappe.get_single("DOTS Integration Settings")
		
		if not settings.enabled:
			frappe.throw("DOTS Integration is not enabled")
		
		if not settings.api_token:
			frappe.throw("API Token is not configured")
		
		if not date:
			date = getdate()
		
		attendance_data = fetch_dots_attendance(settings, date)
		
		if attendance_data:
			processed_count = process_attendance_data(attendance_data, settings)
			
			settings.last_sync_datetime = now_datetime()
			settings.save(ignore_permissions=True)
			frappe.db.commit()
			
			return {
				"success": True,
				"message": f"Successfully processed {processed_count} attendance records for {date}",
				"processed_count": processed_count
			}
		else:
			return {
				"success": True,
				"message": f"No attendance data found for {date}",
				"processed_count": 0
			}
			
	except Exception as e:
		frappe.log_error(f"DOTS Integration Error: {str(e)}", "DOTS Sync Error")
		frappe.throw(f"Error syncing DOTS attendance: {str(e)}")

def fetch_dots_attendance(settings, date):
	"""Fetch attendance data from DOTS API"""
	try:
		token = frappe.utils.password.get_decrypted_password("DOTS Integration Settings", "DOTS Integration Settings", "api_token")
		if not token:
			frappe.throw("API Token is not configured or could not be decrypted")
		
		token = token.strip()
		auth_header = token if token.startswith('Bearer ') else f'Bearer {token}'
			
		headers = {
			'ap-authentication': auth_header,
			'Content-Type': 'application/json',
			'Accept': 'application/json'
		}
		
		response = requests.get(settings.api_url, headers=headers, timeout=30)
		
		if response.status_code == 200:
			data = response.json()
			if data and 'result' in data and data['result']:
				filtered_data = []
				for record_group in data['result']:
					for record in record_group:
						if record.get('date') == str(date):
							filtered_data.append(record)
				return filtered_data
			return []
		elif response.status_code == 401:
			frappe.throw("Authentication failed (401). Please check your API token.")
		elif response.status_code == 403:
			frappe.throw("Access forbidden (403). Your API token may not have sufficient permissions or may be expired.")
		else:
			frappe.throw(f"API request failed with status code: {response.status_code}. Response: {response.text[:200]}")
			
	except requests.exceptions.RequestException as e:
		frappe.throw(f"Network error while fetching DOTS data: {str(e)}")
	except Exception as e:
		frappe.throw(f"Error fetching DOTS attendance: {str(e)}")

def process_attendance_data(attendance_data, settings):
	"""Process DOTS attendance data and create Employee Checkin records"""
	processed_count = 0
	employee_mapping = get_employee_mapping(settings) if settings.use_employee_mapping else {}
	project_mapping = get_project_mapping(settings) if settings.use_project_mapping else {}
	
	for record in attendance_data:
		try:
			dots_emp_id = record.get('empid')
			if not dots_emp_id:
				continue
				
			if settings.use_employee_mapping:
				erpnext_employee = employee_mapping.get(dots_emp_id)
				if not erpnext_employee:
					frappe.log_error(f"No employee mapping found for DOTS Employee ID: {dots_emp_id}", "DOTS Mapping Error")
					continue
			else:
				if frappe.db.exists("Employee", dots_emp_id):
					erpnext_employee = dots_emp_id
				else:
					frappe.log_error(f"Employee with ID '{dots_emp_id}' does not exist in ERPNext", "DOTS Employee Error")
					continue
			
			date_str = record.get('date')
			time_str = record.get('time')
			if not date_str or not time_str:
				continue
				
			datetime_str = f"{date_str} {time_str}"
			checkin_time = get_datetime(datetime_str)
			
			existing_checkin = frappe.db.exists("Employee Checkin", {
				"employee": erpnext_employee,
				"time": checkin_time
			})
			
			if existing_checkin:
				continue
			
			checkin_doc = frappe.new_doc("Employee Checkin")
			checkin_doc.employee = erpnext_employee
			checkin_doc.time = checkin_time
			checkin_doc.log_type = "IN" if record.get('type', '').upper() == "IN" else "OUT"
			checkin_doc.device_id = "DOTS API"
			
			project = record.get('project')
			if project:
				if settings.use_project_mapping:
					mapped_project = project_mapping.get(project)
					if mapped_project:
						checkin_doc.custom_project = mapped_project
					else:
						frappe.logger().warning(f"No project mapping found for DOTS Project: '{project}' for employee {dots_emp_id}")
				else:
					project_exists = frappe.db.exists("Project", project)
					if project_exists:
						checkin_doc.custom_project = project
					else:
						frappe.logger().warning(f"Project '{project}' from DOTS does not exist in ERPNext for employee {dots_emp_id}")
			
			geolocation = record.get('geolocation', '')
			if geolocation and 'Latitude:' in geolocation and 'Longitude:' in geolocation:
				try:
					parts = geolocation.split('||')[0].strip()
					lat_part = parts.split('Latitude:')[1].split(',')[0].strip()
					lon_part = parts.split('Longitude:')[1].strip()
					
					checkin_doc.latitude = float(lat_part)
					checkin_doc.longitude = float(lon_part)
					checkin_doc.geolocation = geolocation
				except (IndexError, ValueError):
					checkin_doc.geolocation = geolocation
			
			checkin_doc.insert(ignore_permissions=True)
			processed_count += 1
			
		except Exception as e:
			frappe.log_error(f"Error processing DOTS record {record}: {str(e)}", "DOTS Processing Error")
			continue
	
	return processed_count

def get_employee_mapping(settings):
	"""Get employee mapping dictionary from settings"""
	mapping = {}
	for row in settings.employee_mapping:
		mapping[row.dots_employee_id] = row.employee
	return mapping

def get_project_mapping(settings):
	"""Get project mapping dictionary from settings"""
	mapping = {}
	for row in settings.project_mapping:
		mapping[row.dots_project_name] = row.project
	return mapping

@frappe.whitelist()
def debug_token_format():
	"""Debug function to check token format"""
	try:
		settings = frappe.get_single("DOTS Integration Settings")
		if not settings.api_token:
			return {"error": "No token configured"}
		
		# Get the decrypted token
		decrypted_token = frappe.utils.password.get_decrypted_password("DOTS Integration Settings", "DOTS Integration Settings", "api_token")
		if not decrypted_token:
			return {"error": "Token could not be decrypted"}
		
		token = decrypted_token.strip()
		return {
			"token_length": len(token),
			"starts_with_bearer": token.startswith('Bearer '),
			"first_20_chars": token[:20] + "..." if len(token) > 20 else token,
			"token_type": "Bearer prefixed" if token.startswith('Bearer ') else "Raw token",
			"encrypted_value": settings.api_token[:20] + "..." if settings.api_token else "None"
		}
	except Exception as e:
		return {"error": str(e)}

@frappe.whitelist()
def test_dots_connection():
	"""Test DOTS API connection"""
	try:
		settings = frappe.get_single("DOTS Integration Settings")
		
		if not settings.api_token:
			return {"success": False, "message": "API Token is not configured"}
		
		# Get the decrypted API token
		token = frappe.utils.password.get_decrypted_password("DOTS Integration Settings", "DOTS Integration Settings", "api_token")
		if not token:
			return {"success": False, "message": "API Token could not be decrypted"}
		
		# Ensure the token doesn't already include "Bearer "
		token = token.strip()
		if token.startswith('Bearer '):
			auth_header = token
		else:
			auth_header = f'Bearer {token}'
			
		headers = {
			'ap-authentication': auth_header,
			'Content-Type': 'application/json',
			'Accept': 'application/json'
		}
		
		response = requests.get(settings.api_url, headers=headers, timeout=10)
		
		if response.status_code == 200:
			data = response.json()
			return {
				"success": True,
				"message": "Connection successful",
				"data_preview": data.get('result', [])[:2] if data.get('result') else []
			}
		else:
			return {
				"success": False,
				"message": f"API request failed with status code: {response.status_code}"
			}
			
	except Exception as e:
		return {"success": False, "message": f"Connection test failed: {str(e)}"}

@frappe.whitelist()
def manual_sync():
	"""Manual sync for today's date"""
	return sync_dots_attendance()

@frappe.whitelist()
def get_sync_status():
	"""Get current sync status and timing information"""
	try:
		settings = frappe.get_single("DOTS Integration Settings")
		
		if not settings.enabled:
			return {
				"status": "Disabled",
				"message": "DOTS Integration is disabled"
			}
		
		if not settings.sync_frequency:
			return {
				"status": "No Frequency",
				"message": "Sync frequency is not configured"
			}
		
		return {
			"status": "Active" if settings.last_sync_datetime else "Ready",
			"sync_frequency": settings.sync_frequency,
			"last_sync": settings.last_sync_datetime,
			"message": f"Syncing {settings.sync_frequency.lower()}" if settings.last_sync_datetime else "Ready for first sync"
		}
	except Exception as e:
		return {"error": str(e)}

def scheduled_sync_check():
	"""Check if it's time to sync based on frequency setting"""
	try:
		settings = frappe.get_single("DOTS Integration Settings")
		
		if not settings.enabled:
			return
		
		if should_sync_now(settings):
			scheduled_sync()
		
	except Exception as e:
		frappe.log_error(f"Scheduled DOTS sync check error: {str(e)}", "DOTS Scheduled Sync Check Error")

def should_sync_now(settings):
	"""Check if sync should run based on frequency and last sync time"""
	if not settings.sync_frequency:
		return False
	
	if not settings.last_sync_datetime:
		return True
	
	now = now_datetime()
	last_sync = get_datetime(settings.last_sync_datetime)
	
	# Check based on the frequency setting
	frequency_map = {
		"Every 4 Minutes": 4,
		"Hourly": 60,
		"Daily": 1440,  # 24 * 60
		"Weekly": 10080,  # 7 * 24 * 60
		"Monthly": 43200  # 30 * 24 * 60 (approximate)
	}
	
	required_interval = frequency_map.get(settings.sync_frequency, 4)  # Default to 4 minutes
	minutes_passed = (now - last_sync).total_seconds() / 60
	
	return minutes_passed >= required_interval

def scheduled_sync():
	"""Scheduled sync function called when it's time to sync"""
	try:
		settings = frappe.get_single("DOTS Integration Settings")
		
		if not settings.enabled:
			return
		
		today = getdate()
		yesterday = today - timedelta(days=1)
		
		sync_dots_attendance(today)
		sync_dots_attendance(yesterday)
		
		frappe.logger().info(f"DOTS scheduled sync completed for {today} and {yesterday}")
		
	except Exception as e:
		frappe.log_error(f"Scheduled DOTS sync error: {str(e)}", "DOTS Scheduled Sync Error")