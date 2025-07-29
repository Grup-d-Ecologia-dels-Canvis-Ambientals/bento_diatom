FROM python:3.12.11-bullseye

WORKDIR /usr/src/app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# COPY data ./
# COPY doa_diatom_model.pth ./
COPY *.py ./
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


RUN python3 create_doa_plus_species_dataset.py w
# RUN bentoml serve
CMD [ "bentoml", "serve" ]