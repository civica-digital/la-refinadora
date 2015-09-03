# ISO-8601

Detects if the data has dates in a ISO 8601 compatible format.

## Setup

```console
docker build -t validadora/iso8601 .
```

## Usage

```console
docker run -it  --name iso -v /tmp/tmp.csv:/tmp/dataset.csv iso8601
```

## License
