# DOTS ERPNext Integration

ERPNext app for automated employee attendance sync with DOTS HR system.

![DOTS Integration Settings](https://github.com/user-attachments/assets/5cf677f1-5f48-4dee-8752-8c1f2e921e19)

![Employee Checkin Records](https://github.com/user-attachments/assets/3b0e8cb1-db29-4081-9be1-a9a9370761e6)

## Features

- **Auto Sync**: Configurable periodic sync from DOTS API
- **Mapping**: Optional employee ID and project name mapping  
- **Geolocation**: GPS coordinates preservation
- **Monitoring**: Sync status and error logging

## Installation

```bash
bench get-app https://github.com/aadhilpm/dot_erpnext.git
bench install-app dot_erpnext
bench restart
```

## Setup

1. Go to **Setup > DOTS Integration Settings**
2. Add API URL and Bearer token
3. Configure employee/project mapping (if needed)
4. Enable integration and set sync frequency
5. Test connection

## Requirements

- ERPNext v15+, Frappe v15+, HRMS
- DOTS HR API access

## License

MIT
