from django.conf.urls import url
from django.views.generic import ListView, DetailView
from .models import Competition

app_name = 'competitions'
urlpatterns = [
                url(r'^$', ListView.as_view(
                                    # queryset=Post.objects.all().order_by("-date")[:25],
                                    queryset=Competition.objects.all().order_by("title")[:25],
                                    template_name="competitions.html")),
                url(r'^(?P<pk>\d+)$', DetailView.as_view(
                                    model=Competition,
                                    template_name="competition.html")),
                url(r'^(?P<pk>\d+)/rank$', DetailView.as_view(
                                    model=Competition,
                                    template_name="competition_rank.html")),
                url(r'^(?P<pk>\d+)/protocol$', DetailView.as_view(
                                    model=Competition,
                                    template_name="competition_protocol.html")),
            ]
