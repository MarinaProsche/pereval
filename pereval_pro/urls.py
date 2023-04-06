
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from pereval_app.views import PerevalViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('submitData', PerevalViewSet.as_view(
        {'get' : 'list', 'post' : 'create'}),
         name='pereval-list'),
    path('submitData/<int:pk>', PerevalViewSet.as_view(
        {'get': 'retrieve', 'patch': 'partial_update',}),
         name='pereval-detail'),
    # path('submitData/', mpass_list_filtered, name='mpass-list-filtered'),
    # path('swagger-ui/', TemplateView.as_view(template_name="swagger-ui.html")),
    # path('redoc/', TemplateView.as_view(
    #     template_name='redoc.html',
    #     extra_context={'schema_url': 'openapi-schema'}
    # ), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)