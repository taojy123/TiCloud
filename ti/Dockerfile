FROM python:3.8.0

#RUN apt-get update && apt-get -y install vim && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo Asia/Shanghai > /etc/timezone

COPY requirements.txt /workspace/requirements.txt
#RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple --trusted-host https://mirrors.aliyun.com
RUN pip install -r requirements.txt -i http://pypi.doubanio.com/simple/
#RUN pip install -r requirements.txt

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
RUN sed -i 's/\r//' /usr/local/bin/entrypoint.sh

COPY . /workspace

EXPOSE 8000

ENTRYPOINT ["entrypoint.sh"]

