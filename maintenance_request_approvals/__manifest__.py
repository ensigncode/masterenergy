{
    "name": "Maintenance Management",
    "depends": [
        "stock",
        "maintenance",
        "hr_maintenance",
        "asset_mro_maintenance_management",
    ],
    "category": "Manufacturing/Maintenance",
    "summary": """This app allow you to manage multiple approvals on maintenance request form""",
    "description": """ Multiple Approvals on Maintenance Request
    
     Please follow Below Steps for right configuration after installing this module: 
         0)- Activate the developers mode.
         
         1)- Go to Settings > User & Companies > Any User. Find the Different provided groups for maintenance request approvals.
         
         2)- Create different users to the provided groups found in the previous point (e.g. Store User will have store true in its user).
         
         3)- (FYI) Any user can create maintenance request but the User with group 'User' checked can send it to the first HOD approval.
         
         4)- Set the sequence of the newly added stages from Maintenance > Configuration > Maintenance Stages by dragging the stage with handle just before its name.
         
         5)- (FYI) Sequence should be good like New Request, HOD, Audit, Plant Manager, Maintenance Officer, Store Officer, Repaired, Scrap, Completed.
         
         6)- Create your maintenance request with the User Department's User and you will see Send to HOD just after creating.
         
         7)- Similarly every user will see its approval button with its name. User will press the button and request will move to the next approval.
         
         8)- When the maintenance office done its work will press the button Done Work and move the request to Repaired stage.
         
         9)- User will then make it to the completed stage.
         
         10- Email Configuration is the same as previous.
         
     """,
    "author": "Hamza Ilyas",
    "website": "hamza.ilyaaaas@gmail.com",
    # 'images': ['static/description/icon.png'],
    "data": [
        "security/maintenance_approval_groups.xml",
        # 'security/maintenance_request_security.xml',
        "views/maintenance_request_view.xml",
        "views/config_setting_ext.xml",
        "data/new_maintainance_stages.xml",
    ],
    "installable": True,
}
