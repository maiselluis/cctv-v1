from .models import UserActionLog

class UserActionLogMixin:
    action_type = None
    extra_info = None

    def log_action(self, request):
       # print(f"[LOG DEBUG] Action logged: {self.action_type} by {request.user}")

        if self.action_type and request.user.is_authenticated:
            UserActionLog.objects.create(
                user=request.user,
                action=self.action_type,
                url=request.path,
                extra_info=self.extra_info or ""
            )
