from django.db import models

from users.models import CustomUser


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='messages_received', on_delete=models.CASCADE)
    content = models.TextField()
    message_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} to {self.receiver}: {self.content[:10]}'
