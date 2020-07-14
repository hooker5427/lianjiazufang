FROM alpine:3.11
RUN echo -e 'http://mirrors.aliyun.com/alpine/v3.11/main/\nhttp://mirrors.aliyun.com/alpine/v3.11/community/' > /etc/apk/repositories
RUN apk add --update --no-cache gcc g++ musl-dev libffi-dev libxml2-dev libxslt-dev jpeg-dev curl-dev make python3 python3-dev tzdata git curl \
&& cp /usr/share/zoneinfo/Asia/Chongqing /etc/localtime && echo 'Asia/Chongqing' > /etc/timezone && apk del tzdata \
&& python3 -m pip install -i https://pypi.doubanio.com/simple/ --upgrade pip \
&& python3 -m pip install -i https://pypi.doubanio.com/simple/ -r requirements.txt
WORKDIR spider
ADD . /spider
COPY scrapyd.conf /etc/scrapyd/
RUN  python3 -m pip install -r requirements.txt
WORKDIR lianjiaSpider
CMD python start.py
