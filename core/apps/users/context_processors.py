from .models import Profile

def add_profile_to_context(request):
    # Return an empty dictionary if the user is not authenticated
    if not request.user.is_authenticated:
        return {}

    try:
        # Try to get the profile linked to the current user
        profile = request.user.profile
    except Profile.DoesNotExist:
        # If a profile doesn't exist, create one
        profile = Profile.objects.create(user=request.user)

    return {'profile': profile}