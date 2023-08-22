from django.db import models
from django.contrib.auth.models import User


# Create message model
class Message(models.Model):
    user = models.ForeignKey(
        User,
        related_name='megs',
        on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user} -> {self.created_at:%d-%m-%Y %H:%M}: {self.body:30}'


# symmetrical = False significa que eu posso seguir alguém, mas a pessoa não precisa me seguir necessariamente
# related_name faz a relação contrária, verifica quem está te seguindo
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self", related_name="followed_by",
        symmetrical=False,
        blank=True
    )
    date_modified = models.DateTimeField(User, auto_now=True)

    def __str__(self) -> str:
        return f'Perfil: <{self.user}>'
