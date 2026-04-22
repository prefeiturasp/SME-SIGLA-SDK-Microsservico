class AuditlogJWTMiddleware:
    """
    Substitui o AuditlogMiddleware padrão resolvendo o usuário diretamente
    do token JWT antes de setar o actor do auditlog.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = self._resolve_user(request)
        if user and getattr(user, "is_authenticated", False):
            from auditlog.context import set_actor

            with set_actor(user):
                return self.get_response(request)
        return self.get_response(request)

    def _resolve_user(self, request):
        try:
            from rest_framework_simplejwt.authentication import JWTAuthentication

            result = JWTAuthentication().authenticate(request)
            if result is not None:
                return result[0]  # (user, token)
        except Exception:
            return None
        return None

