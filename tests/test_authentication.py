import pytest
from django.test import override_settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from sigla_sdk.autenticacao.authentication import ApiKeyAuthentication, UsuarioApiKey

factory = APIRequestFactory()
auth = ApiKeyAuthentication()


def _request(api_key: str | None = None) -> Request:
    kwargs = {"HTTP_X_API_KEY": api_key} if api_key is not None else {}
    return Request(factory.get("/", **kwargs))


@override_settings(API_KEY="secret-key")
def test_autentica_com_api_key_valida():
    user, token = auth.authenticate(_request("secret-key"))
    assert isinstance(user, UsuarioApiKey)
    assert token is None


@override_settings(API_KEY="")
def test_falha_quando_api_key_nao_configurada():
    with pytest.raises(AuthenticationFailed, match="não configurada"):
        auth.authenticate(_request("qualquer"))


@override_settings(API_KEY="secret-key")
def test_falha_quando_header_ausente():
    with pytest.raises(AuthenticationFailed, match="não informada"):
        auth.authenticate(_request())


@override_settings(API_KEY="secret-key")
def test_falha_quando_api_key_invalida():
    with pytest.raises(AuthenticationFailed, match="inválida"):
        auth.authenticate(_request("errada"))
