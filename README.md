# DSCM034

Mini service that deploys opencv image detection models. It comes with the pretrained weights for yolov4.

To interact with the model use the swagger ui on the `/docs` endpoint.

## How to build

Clone and navigate to the directory of the repository. Build the docker image:
```sh
docker build -t <name>:<tag> .
```

## How to run

The default configuration uses port 8000. To start the container on localhost port-forward port 8000:
```sh
docker run -d --rm -p 8000:8000 <name>:<tag>
```

This will start the container in detached mode and removes it when it stops. To view the logs of the server remove the argument: `-d`.

It is possible to use a different opencv model by attaching the weights, config and labels as volumes when running starting the container:

```sh
docker run -d --rm -p 8000:8000 -v <volume-path>:/opt/app/config <name>:<tag>
```

The `<volume-path>` must contain the files `model.weights` the pretrained weights, `model.cfg` the opencv configuration and `model.labes` containg the labels in a line separated file.

Depending on the model different image input sizes can be set with the environment variables `IMG_WIDTH` (int), `IMG_HEIGHT` (int) and `IMG_SCALING` (float)

Confidence thresholds can be set with the environment variables `CONFIDENCE` (float) and `NMS_CONFIDENCE` (float). The default value for both is 0.7.
