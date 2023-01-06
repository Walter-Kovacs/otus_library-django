from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class AdminPermissionMixin(LoginRequiredMixin):

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('/')

        return super().get(request, *args, **kwargs)
