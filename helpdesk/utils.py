from django.contrib.auth.decorators import user_passes_test

def group_required(*group_names):
    """
    Decorator for views that checks if the user is in at least one of the given groups.
    Superusers are allowed by default.
    """
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) or u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)
