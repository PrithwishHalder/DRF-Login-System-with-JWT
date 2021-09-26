from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class OTP(models.Model):
  user = models.OneToOneField(
      User, on_delete=models.CASCADE, related_name="user")
  otp = models.CharField(max_length=12, blank=True, null=True)

  def __str__(self):
    return self.otp

  class Meta:
    db_table = "OTP"
