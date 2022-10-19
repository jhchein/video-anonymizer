# Commands

## Build the image

```PowerShell
docker image build -t video-anonymize-extract:1 .
```

## Run the container

```PowerShell
docker container run video-anonymize-extract:1 --inputblob "blob-uri-with-sas-token" --connectionstring "your-connection-string"
```
