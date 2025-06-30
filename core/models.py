# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Position(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Candidate(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.position.name}"

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'position')

    def __str__(self):
        nickname = getattr(self.user.profile, 'nickname', '')
        return f"{self.user.username} ({nickname}) voted for {self.candidate.name} ({self.position.name})"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = student_id = models.CharField(
        max_length=7,
        unique=True,
        validators=[RegexValidator(r'^\d+$', 'Only numeric characters are allowed.')]
    )
    nickname = models.CharField(max_length=50, default='temp')
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.student_id