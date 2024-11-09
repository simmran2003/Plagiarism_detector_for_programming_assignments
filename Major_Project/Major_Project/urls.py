"""
URL configuration for Major_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # Import include
# from AST_based_approach.views import home,compare_code,compare_code_view  # Import the home view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("AST_based_approach.urls")),
    # path("", home, name="home"),  # Root URL pointing to home view
    # path("AST_based_approach/", include("AST_based_approach.urls")),  # Including app's URLs
    # path('', home, name='home'),  # Main page
    # path('compare/', compare_code, name='compare_code'),
]

