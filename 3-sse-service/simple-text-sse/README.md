# Echo Service Using Python-Flask

## Use case

When the service is invoked with a message, the service will respond with the same message received via an HTTP POST.

## How to Run

`uvicorn main:app --reload`

## Test the endpoint

```
curl -L 'http://localhost:8000/stream"'
```

```
curl -L 'http://localhost:8000/'
```
