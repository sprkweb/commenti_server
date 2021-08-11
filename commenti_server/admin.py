from django.contrib import admin
from django.utils.translation import gettext_lazy as _

class CommentiAdminSite(admin.AdminSite):
    site_header = _('Commenti administration')
    site_title = _('Commenti administration')
    site_url = None
    index_title = _('Home')
