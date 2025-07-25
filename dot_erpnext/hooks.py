app_name = "dot_erpnext"
app_title = "Dot Erpnext"
app_publisher = "Aadhil Badeel Technology"
app_description = "This app is the integration of DOTS Face app to erpnext"
app_email = "support@badeeltechnology.com"
app_license = "mit"

# Fixtures
# --------
fixtures = [
	{
		"doctype": "Custom Field",
		"filters": [
			["name", "in", ["Employee Checkin-custom_project"]]
		]
	}
]

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "dot_erpnext",
# 		"logo": "/assets/dot_erpnext/logo.png",
# 		"title": "Dot Erpnext",
# 		"route": "/dot_erpnext",
# 		"has_permission": "dot_erpnext.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/dot_erpnext/css/dot_erpnext.css"
# app_include_js = "/assets/dot_erpnext/js/dot_erpnext.js"

# include js, css files in header of web template
# web_include_css = "/assets/dot_erpnext/css/dot_erpnext.css"
# web_include_js = "/assets/dot_erpnext/js/dot_erpnext.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "dot_erpnext/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "dot_erpnext/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "dot_erpnext.utils.jinja_methods",
# 	"filters": "dot_erpnext.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "dot_erpnext.install.before_install"
after_install = "dot_erpnext.dot_erpnext.setup.after_install"

# Uninstallation
# ------------

# before_uninstall = "dot_erpnext.uninstall.before_uninstall"
# after_uninstall = "dot_erpnext.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "dot_erpnext.utils.before_app_install"
# after_app_install = "dot_erpnext.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "dot_erpnext.utils.before_app_uninstall"
# after_app_uninstall = "dot_erpnext.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "dot_erpnext.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"dot_erpnext.dot_erpnext.api.dots_integration.scheduled_sync_check"
	]
}

# Testing
# -------

# before_tests = "dot_erpnext.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "dot_erpnext.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "dot_erpnext.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["dot_erpnext.utils.before_request"]
# after_request = ["dot_erpnext.utils.after_request"]

# Job Events
# ----------
# before_job = ["dot_erpnext.utils.before_job"]
# after_job = ["dot_erpnext.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"dot_erpnext.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

