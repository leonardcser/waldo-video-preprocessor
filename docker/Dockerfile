FROM jjanzic/docker-python3-opencv

RUN useradd -ms /bin/bash user
USER user

WORKDIR /home/user

COPY ./requirements/docker-requirements.txt .
RUN pip install -r docker-requirements.txt && rm docker-requirements.txt

COPY ./processing ./processing
COPY ./utils ./utils
COPY ./main.py ./main.py
COPY ./variables.py ./variables.py

ENTRYPOINT [ "python", "main.py"]