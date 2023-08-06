from django.urls import path

try:
    import fints
except ModuleNotFoundError:
    fints = None

urlpatterns = []

if fints:
    from .fints.views import FinTSView

    urlpatterns.append(path("fints/conversation/", FinTSView.as_view(), name="fints_conversation"))
