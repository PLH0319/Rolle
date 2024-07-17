# Assuming your project's main urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # for login/logout urls
    path('accounts/', include('accounts.urls')),  # for login/logout urls
    path('musical_theater/', include('musical_theater_info.urls'))
    # other urls
]
