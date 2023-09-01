from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_query_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    complete = models.BooleanField(default=False)
    created = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['complete']
