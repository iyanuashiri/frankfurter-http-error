# Preserve upstream HTTP errors from the Frankfurter API

## Background

The currency endpoints depend on the Frankfurter API to retrieve exchange rate information.

Currently, when the external service cannot be reached, the application raises a `FrankfurterException`. This exception is not translated into an appropriate HTTP response, causing clients to receive a generic `500 Internal Server Error`.

## Your Task

Update the implementation so that failures from the external currency service return the appropriate HTTP response instead of an internal server error.

For example, if the upstream service is unavailable, the API should return:

- HTTP 503 Service Unavailable

instead of

- HTTP 500 Internal Server Error

Do not change the public API of the application.

Existing successful requests should continue to behave exactly as before.