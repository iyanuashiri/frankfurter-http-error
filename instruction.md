# Bug: Currency Conversion Silently Returns Bad Data on Invalid Currency Codes

When a request is made with an invalid or unsupported currency code, the
external Frankfurter API returns an error response. Instead of surfacing
that as a clear error to our users, something downstream is returning
malformed or unexpected data without raising any exception.

Investigate `/app/frankfurter/rest_adapter.py`, specifically how HTTP
error responses from the external API are detected and handled.

Error responses from the external API (4xx/5xx) must always raise an
appropriate exception — never be silently treated as successful data.
Successful (2xx) responses must keep working exactly as they do now, and
don't change any method signatures. Assume there's a broader test suite
covering this and other parts of the app, so don't break anything else
along the way.