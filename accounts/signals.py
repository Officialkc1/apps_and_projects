from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail

from accounts.models import CustomUser

@receiver(post_save, sender=AbstractUser)
def send_activation_email(sender, instance, created, **kwargs):

    if created:
        message =f"""Hello, {instance.first_name}.
        Thank you for signing up on our platform. We hope you enjoy it here.
        
        
        Regards,
        The Django Team.
        """
        send_mail(subject="Your Account Has Been Created",
                  message = message,
                  recipient_list=[instance.email],
                  from_email = "list@todo.com")