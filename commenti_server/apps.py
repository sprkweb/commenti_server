from django.contrib.admin.apps import AdminConfig

class CommentiAdminConfig(AdminConfig):
    default_site = 'commenti_server.admin.CommentiAdminSite'
