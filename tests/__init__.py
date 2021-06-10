"""
All routes:
main_bp:
    `/` index_page
    `/logout` logout_page

user_bp (login_required):
    `/report` report_page
    `/dashboard` dashboard_page
    `/user_setting` user_setting_page

admin_bp (admin_required):
    `/admin_dashboard` dashboard_page
    `system` system_page
    `/manage_user` manage_user_page
    `/backup` backup_page

    `/admin_dashboard_backend` admin_dashboard_backend_page
    `system_backend` system_backend_page
    `/manage_user_backend` manage_user_backend_page
    `/backup_backend` backup_backend_page
    `/backup/<filename>` get_backup_file
"""