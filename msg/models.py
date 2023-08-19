from django.db import models
from django.contrib.auth.models import User



# symmetrical = False significa que eu posso seguir alguém, mas a pessoa não precisa me seguir necessariamente
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self", related_name="followed_by",
        symmetrical=False,
        blank=True
    )

    def __str__(self) -> str:
        return f'Perfil: <{self.user}>'
