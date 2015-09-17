# Column check
Validates from a representative sample size that data columns are complete.

## Setup

```console
docker build -t validadora/columcheck .
```

## Usage

```console
docker run -it  --name column -v /tmp/tmp.csv:/tmp/dataset.csv columncheck
```

## License
