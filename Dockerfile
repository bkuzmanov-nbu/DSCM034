from python:3.12

COPY . .

RUN mkdir -p "/opt/app/config" \
  && mv yolo/yolov4-tiny.weights /opt/app/config/model.weights \
  && mv yolo/yolov4-tiny.cfg /opt/app/config/model.cfg \
  && mv yolo/labels /opt/app/config/model.labels \
  && mv server.py /opt/app/server.py \
  && apt-get update && apt-get install ffmpeg libsm6 libxext6  -y \
  && pip install --no-cache-dir -r requirements.txt

ENV WEIGHTS_PATH=/opt/app/config/model.weights \
 CONFIG_PATH=/opt/app/config/model.cfg \
 LABELS_PATH=/opt/app/config/model.labels

WORKDIR /opt/app

CMD ["fastapi", "run", "server.py"]
