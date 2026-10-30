
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def home(request):
    return HttpResponse(
        "<h1>API is running</h1>"
        "<p>Click a link instead of typing the URL:</p>"
        "<ul>"
        '<li><a href="/api/v1/students/">/api/v1/students/</a> &mdash; students API (browsable page)</li>'
        '<li><a href="/students/">/students/</a> &mdash; plain text demo</li>'
        '<li><a href="/admin/">/admin/</a> &mdash; Django admin</li>'
        "</ul>"
    )


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('students/', include('students.urls')),
    path('api/v1/', include('api.urls'))
]