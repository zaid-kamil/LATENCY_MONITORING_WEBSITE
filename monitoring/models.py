from django.db import models

class Website(models.Model):
    url = models.URLField(max_length=200, unique=True)
    check_frequency = models.IntegerField(help_text='Frequency in minutes')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.url
    
class Measurement(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    latency = models.FloatField(default=0.0)
    status_code = models.IntegerField(default=200)
    error = models.TextField(null=True)


    def __str__(self):
        return f'{self.website.url} at {self.timestamp}: {self.latency} ms'

class Notification(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return f'Notification for {self.website.url} at {self.timestamp}: {self.message}'

class Feedback(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f'Feedback for {self.website.url} at {self.timestamp}: {self.message}'
    
class Issue(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('closed', 'Closed')], default='open')

    def __str__(self):
        return f'Issue for {self.website.url} at {self.timestamp}: {self.message}'
    
class contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name

class Subscriber(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email



