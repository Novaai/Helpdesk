from django.contrib.auth.models import Group

# Groups to exclude from "is_admin" status
EXCLUDED_ADMIN_GROUPS = [
    "Helpdesk Admins",
    "Inventory Admins",
]

def is_admin_excluding_groups(user, excluded_groups=None):
    """
    Returns True if user is an 'admin',
    Returns false if user is not admin or if they are in any of the excluded groups.
    """
    if not user or not user.is_authenticated:
        return False

    if excluded_groups is None:
        excluded_groups = EXCLUDED_ADMIN_GROUPS

    # Superusers are always admins unless explicitly excluded
    if user.is_superuser:
        return not user.groups.filter(name__in=excluded_groups).exists()

    # Example: treat members of "admins" group as admins
    is_in_admin_group = user.groups.filter(name="admins").exists()

    # If not in admin group → not an admin
    if not is_in_admin_group:
        return False

    # Exclude if in any forbidden group
    in_excluded = user.groups.filter(name__in=excluded_groups).exists()
    return not in_excluded
