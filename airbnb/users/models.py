from django.db import models
from db.models import BaseModel
from django.contrib.auth.models import User

class Chat(BaseModel):
    owner = models.ForeignKey(
        User,
        related_name='chats',
        help_text="User who created this conversation",
        on_delete=models.CASCADE
    )

    topic = models.CharField(
        help_text='topic of conversation',
        max_length=255,
        null=True,
        blank=True
    )

    
    # todo: this should eventually extend to a through field where we define archived / chat status
    participants = models.ManyToManyField(
        User,
        related_name='chat_participants')

    def __str__(self):
        return f'chat about {self.topic}'


class Message(BaseModel):
    chat = models.ForeignKey(
        'users.Chat',
        related_name='messages',
        help_text='Chat from which message belongs',
        on_delete=models.CASCADE
    )

    sender = models.ForeignKey(
        User,
        related_name='messages',
        help_text="Sender of this message",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    message = models.TextField()

    read_by = models.ManyToManyField(
        User,
        related_name='message_recipients',
        blank=True
    )

    @property
    def receiver(self):
        return self.chat.participants

    def __str__(self):
        return f'{self.id} : {self.sender} sends message to {self.receiver}'

