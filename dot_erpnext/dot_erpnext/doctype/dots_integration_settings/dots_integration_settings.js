frappe.ui.form.on('DOTS Integration Settings', {
	refresh: function(frm) {
		// Add custom buttons
		frm.add_custom_button(__('Debug Token'), function() {
			frappe.call({
				method: 'dot_erpnext.dot_erpnext.api.dots_integration.debug_token_format',
				callback: function(r) {
					frappe.msgprint({
						title: __('Token Debug Info'),
						message: '<pre>' + JSON.stringify(r.message, null, 2) + '</pre>',
						indicator: 'blue'
					});
				}
			});
		});

		frm.add_custom_button(__('Test Connection'), function() {
			frappe.call({
				method: 'dot_erpnext.dot_erpnext.api.dots_integration.test_dots_connection',
				callback: function(r) {
					if (r.message.success) {
						frappe.msgprint({
							title: __('Connection Test'),
							message: __('Connection successful! API is working properly.'),
							indicator: 'green'
						});
					} else {
						frappe.msgprint({
							title: __('Connection Test Failed'),
							message: r.message.message,
							indicator: 'red'
						});
					}
				}
			});
		});

		frm.add_custom_button(__('Manual Sync'), function() {
			frappe.call({
				method: 'dot_erpnext.dot_erpnext.api.dots_integration.manual_sync',
				callback: function(r) {
					if (r.message.success) {
						frappe.msgprint({
							title: __('Sync Completed'),
							message: r.message.message,
							indicator: 'green'
						});
						frm.reload_doc();
					} else {
						frappe.msgprint({
							title: __('Sync Failed'),
							message: r.message.message || 'Unknown error occurred',
							indicator: 'red'
						});
					}
				}
			});
		});

		frm.add_custom_button(__('Sync Status'), function() {
			frappe.call({
				method: 'dot_erpnext.dot_erpnext.api.dots_integration.get_sync_status',
				callback: function(r) {
					let info = r.message;
					let message = '';
					let indicator = 'blue';
					
					if (info.error) {
						message = `Error: ${info.error}`;
						indicator = 'red';
					} else if (info.status === 'Disabled') {
						message = info.message;
						indicator = 'orange';
					} else if (info.status === 'Ready') {
						message = `${info.message}<br><strong>Sync Frequency:</strong> ${info.sync_frequency_minutes} minutes`;
						indicator = 'blue';
					} else if (info.status === 'Active') {
						let hours = Math.floor(info.sync_frequency_minutes / 60);
						let minutes = info.sync_frequency_minutes % 60;
						let freq_text = hours > 0 ? `${hours}h ${minutes}m` : `${minutes}m`;
						
						message = `<strong>Status:</strong> ${info.status}<br>`;
						message += `<strong>Frequency:</strong> ${freq_text}<br>`;
						message += `<strong>Last Sync:</strong> ${moment(info.last_sync).format('YYYY-MM-DD HH:mm:ss')}<br>`;
						message += `<strong>Next Sync:</strong> ${moment(info.next_sync).format('YYYY-MM-DD HH:mm:ss')}<br>`;
						
						if (info.overdue) {
							message += `<span style="color: red;"><strong>Status:</strong> Overdue</span>`;
							indicator = 'red';
						} else {
							message += `<strong>Minutes to Next:</strong> ${Math.round(info.minutes_to_next_sync)}`;
							indicator = 'green';
						}
					}
					
					frappe.msgprint({
						title: __('Sync Status'),
						message: message,
						indicator: indicator
					});
				}
			});
		});

		// Add sync status indicator
		if (frm.doc.last_sync_datetime && frm.doc.sync_frequency) {
			let last_sync = moment(frm.doc.last_sync_datetime);
			let time_diff = moment().diff(last_sync, 'minutes');
			let status_color = time_diff > frm.doc.sync_frequency ? 'red' : 'green';
			
			frm.dashboard.add_indicator(__('Last Sync: {0}', [last_sync.fromNow()]), status_color);
			
			// Show next sync time
			let next_sync = moment(frm.doc.last_sync_datetime).add(frm.doc.sync_frequency, 'minutes');
			let next_sync_color = moment().isAfter(next_sync) ? 'orange' : 'blue';
			frm.dashboard.add_indicator(__('Next Sync: {0}', [next_sync.fromNow()]), next_sync_color);
		}
	},

	enabled: function(frm) {
		if (frm.doc.enabled && !frm.doc.api_token) {
			frappe.msgprint(__('Please configure API Token before enabling the integration'));
			frm.set_value('enabled', 0);
		}
	},

	use_employee_mapping: function(frm) {
		if (!frm.doc.use_employee_mapping) {
			frappe.msgprint({
				title: __('Direct Employee ID Matching'),
				message: __('DOTS Employee IDs will be matched directly with ERPNext Employee IDs. Make sure the Employee IDs are identical in both systems.'),
				indicator: 'blue'
			});
		}
	},

	use_project_mapping: function(frm) {
		if (!frm.doc.use_project_mapping) {
			frappe.msgprint({
				title: __('Direct Project Name Matching'),
				message: __('DOTS Project names will be matched directly with ERPNext Project names. Make sure the Project names are identical in both systems.'),
				indicator: 'blue'
			});
		}
	},

	sync_frequency: function(frm) {
		if (frm.doc.sync_frequency) {
			if (frm.doc.sync_frequency < 5) {
				frappe.msgprint({
					title: __('Invalid Frequency'),
					message: __('Sync frequency cannot be less than 5 minutes for system performance reasons.'),
					indicator: 'red'
				});
				frm.set_value('sync_frequency', 5);
			} else {
				// Show helpful message about sync frequency
				let hours = Math.floor(frm.doc.sync_frequency / 60);
				let minutes = frm.doc.sync_frequency % 60;
				let time_str = hours > 0 ? `${hours} hour(s) and ${minutes} minute(s)` : `${minutes} minute(s)`;
				
				frappe.show_alert({
					message: __('DOTS attendance will sync every {0}', [time_str]),
					indicator: 'green'
				});
			}
		}
	}
});