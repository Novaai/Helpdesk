def group_flags(request):
    """Adds group-based permission flags to all templates."""
    if not request.user.is_authenticated:
        return {
            "is_inventory_admin": False,
            "is_inventory_user": False,
            "is_helpdesk_admin": False,
            "is_helpdesk_user": False,
        }

    groups = set(request.user.groups.values_list("name", flat=True))

    return {
        "is_inventory_admin": "Inventory Admins" in groups,
        "is_inventory_user": "Inventory Users" in groups,
        "is_helpdesk_admin": "Helpdesk Admins" in groups,
        "is_helpdesk_user": "Helpdesk Users" in groups,
    }

