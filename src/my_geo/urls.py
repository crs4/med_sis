# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2017 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

#from django.contrib import admin
from geonode.urls import urlpatterns as geonode_urlpatterns
from django.urls import path, include
#from django.conf.urls import url
#from django.views.generic import TemplateView
#from django.conf import settings
#from django.conf.urls.static import static

urlpatterns = [
    # Web Application endpoint
    path("backoffice/", include('backoffice.urls')),

    # API endpoints
    path('api/backoffice/', include('backoffice_api.urls')),
] + geonode_urlpatterns

"""
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

* Aggiunge agli URL le regole per gestire e servire automaticamente 
i file media (immagini caricate, file, ecc.) usando il server di sviluppo Django.

* Questo permette di accedere ai file in MEDIA_ROOT attraverso l'URL MEDIA_URL in modalità sviluppo, 
evitando di configurare server esterni come Nginx o Apache.

"""
    



"""
# You can register your own urlpatterns here
urlpatterns = [
    url(r'^/?$',
        homepage,
        name='home'),
 ] + urlpatterns
"""
