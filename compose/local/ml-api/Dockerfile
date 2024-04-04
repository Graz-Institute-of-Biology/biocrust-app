FROM anibali/pytorch:2.0.1-cuda11.8-ubuntu22.04

RUN apt-get update
RUN apt install nano
#
RUN git clone https://github.com/Graz-Institute-of-Biology/cc-machine-learning ml-api

# 
RUN pip install --no-cache-dir --upgrade -r /app/ml-api/fast_api/requirements.txt
RUN pip install albumentations
RUN pip install --no-binary imgaug imgaug
RUN pip install opencv-python-headless

ARG BUILD_ENVIRONMENT=local
ENV BUILD_ENV ${BUILD_ENVIRONMENT}
# 
# CMD ["python", "/ml-api/main.py"]
ENTRYPOINT [ "python", "/app/ml-api/fast_api/main.py" ]