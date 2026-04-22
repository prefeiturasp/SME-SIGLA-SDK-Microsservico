# sigla-sdk

SDK compartilhado para microsserviços SIGLA.

## Uso

- **HTTP client com headers automáticos**:

```python
from sigla_sdk.http.api_client import http_client
```

- **Formatter JSON com correlation id**:

```python
from sigla_sdk.logging.json_formatter import CustomJsonFormatter
```

- **Middlewares Django**:

```python
from sigla_sdk.django.middlewares import CorrelationIdMiddleware, AuditlogJWTMiddleware
```