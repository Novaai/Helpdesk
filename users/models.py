from django.db import models

# Create your models here.
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models

class RoleRequest(models.Model):
    STATUS_CHOICES = [("pending","Pending"),("approved","Approved"),("rejected","Rejected")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="role_requests")
    requested_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="requested_roles")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    decided_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="role_requests_decided"
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user","requested_group","status"],
                condition=models.Q(status="pending"),
                name="uniq_pending_request_per_user_group",
            )
        ]

    def __str__(self):
        return f"{self.user.username} → {self.requested_group.name} ({self.status})"
