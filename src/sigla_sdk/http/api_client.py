import requests

from sigla_sdk.context import get_auth_header, get_correlation_id


class ServiceSession(requests.Session):
    """
    requests.Session que injeta automaticamente headers de rastreamento e
    autenticação em todas as chamadas de saída, a partir do contexto
    da thread corrente (preenchido pelo CorrelationIdMiddleware).

    Usa setdefault() para nunca sobrescrever headers definidos explicitamente
    pelo chamador.
    """

    def request(self, method, url, *args, **kwargs):
        headers = kwargs.pop("headers", {}) or {}

        cid = get_correlation_id()
        if cid:
            headers.setdefault("X-Correlation-ID", cid)

        auth = get_auth_header()
        if auth:
            headers.setdefault("Authorization", auth)

        kwargs["headers"] = headers
        return super().request(method, url, *args, **kwargs)


http_client = ServiceSession()
