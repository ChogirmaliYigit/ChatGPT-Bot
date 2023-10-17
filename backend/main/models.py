from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    telegram_id = models.PositiveBigIntegerField(unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.full_name} - {self.telegram_id} - @{self.username}"

    class Meta:
        verbose_name = "Telegram User"
        db_table = "users"


class Chat(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        if self.title:
            return self.title
        else:
            return f"{self.id} - chat"

    class Meta:
        db_table = "chats"


class Message(models.Model):
    USER = "user"
    ASSISTANT = "assistant"
    ROLES = (
        (USER, "User"),
        (ASSISTANT, "Assistant")
    )

    role = models.CharField(max_length=20, choices=ROLES, default=USER)
    content = models.TextField()
    chat = models.ForeignKey(Chat, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.role} - {self.chat.title}"

    class Meta:
        db_table = "messages"
