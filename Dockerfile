FROM alpine
RUN apk add --no-cache bash git python3 zbar jpeg-dev zlib-dev python3-dev
RUN pip3 install flask alembic
RUN mkdir /TelegramEDT
RUN git clone https://github.com/flifloo/TelegramEDT.git /TelegramEDT
RUN apk add --no-cache --virtual .build-deps build-base linux-headers
RUN pip3 install -r /TelegramEDT/requirements.txt
RUN apk del .build-deps
COPY ./app.py /root/app.py
CMD python3 /root/app.py
