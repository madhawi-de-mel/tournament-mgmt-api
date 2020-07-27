import json

from django.utils import timezone

from management_app.models import UserProfile
from management_app.serializers import UserSerializer


def get_site_statistics():
    """Returns user site login statistics"""
    profiles = UserProfile.objects.all()
    mapped_profiles = []
    for profile in profiles:
        # if user's current status is logged in, then time from last login to now is added to time spent
        if profile.login_status:
            profile.time_spent = profile.time_spent + (timezone.now() - profile.user.last_login).seconds / 60
        mapped_profiles.append(UserSerializer.get_dump_object(profile))
    return json.dumps(mapped_profiles)
