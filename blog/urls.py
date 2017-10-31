from django.conf.urls import url, include
from . import views
from allauth.account.decorators import login_required

urlpatterns = [
    url(r'^$', login_required(views.Graph.as_view()), name='graph'),
]
