from django.urls import path
from .views import AIFeedbackView

urlpatterns = [
    path('', AIFeedbackView.as_view(), name='ai-feedback'),
]