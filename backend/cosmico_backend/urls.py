from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, JsonResponse

def root_view(request):
    return HttpResponse("Cosmico backend is running", status=200)

def health_view(request):
    return JsonResponse({"status": "ok"}, status=200)

def check_view(request):
    return HttpResponse("Routing is working!", status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('check/', check_view),
    path('', root_view),
    path('health/', health_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
