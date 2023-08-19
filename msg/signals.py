from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile



# Cria um perfil, automaticamente, quando se cria um usuário
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile.objects.create(user=instance)
        user_profile.save()

        # Ao criar o perfil, ele automaticamente irá se seguir
        user_profile.follows.set([instance.profile.id])
        user_profile.save()


# Faz a mesma coisa do receiver
# post_save.connect(create_profile, sender=User)