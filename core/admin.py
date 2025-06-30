from django.contrib import admin
from .models import Position, Candidate, Vote, Profile

admin.site.register(Position)
admin.site.register(Candidate)
admin.site.register(Vote)
admin.site.register(Profile)
