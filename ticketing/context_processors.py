def is_helpdesk_admin(request):
    user = request.user
    is_admin = (
        user.is_authenticated and
        (user.is_superuser or user.groups.filter(name='Helpdesk Admins').exists())
    )
    return {'is_helpdesk_admin': is_admin}
