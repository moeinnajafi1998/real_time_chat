from django.db import models
from django.contrib.auth.models import User

class PrivateChat(models.Model):
    user1 = models.ForeignKey(User, related_name='chats_initiated', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='chats_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_room_name(self):
        return f'chat_{min(self.user1.id, self.user2.id)}_{max(self.user1.id, self.user2.id)}'
