# maigret-adapter

Connecting Maigret with other tools.

## Usage

```sh
./run.py
```

You will start maigret-adapter service at `localhost:8080`.
Now you can use API interface for maigret:

```sh
curl localhost:8080 -s | jq                                                               ~
{
  "maigret-adapter": "0.0.1",
  "usage": "/check/{service}/{site}/{identifier}",
  "services": [
    "test_service",
    "mailcat"
  ]
}
```

## Testing

You have to install Maigret first.

```sh
./test.sh
```

## How to register you service

1. Use `integrations/test_adapter.py` as a template.

1. Add import to `integrations/__init__.py`

1. Register adapter in `run.py`

1. Run server and make health-check of your service with the name used in `run.py`:
```sh
curl localhost:8080/sites/<NAME> -v
```

## Scheme

![Maigret-adapter scheme](https://raw.githubusercontent.com/soxoj/maigret-adapter/main/scheme.png)
