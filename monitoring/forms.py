from .models import Feedback, Measurement, Notification, Website, Issue
from django import forms

class FeedbackForm(forms.ModelForm):
    input_name = forms.CharField(max_length=100)  # Add this line
    class Meta:
        model = Feedback
        fields = ['input_name','website', 'message', ]


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['website','message', 'user', 'status']

class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        fields =[ 'url', 'check_frequency'] 

class Measurement:
    class Meta:
        model = Measurement
        fields = '__all__'

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'       
