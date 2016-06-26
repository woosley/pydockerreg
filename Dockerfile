FROM python:3.5.1
MAINTAINER Woosley Xu <woosley.xu@gmail.com>

ADD requirements.txt /tmp/pydockerreg/
RUN cd /tmp/pydockerreg && pip install -r requirements.txt

ADD setup.py /tmp/pydockerreg/
ADD README.md /tmp/pydockerreg/
ADD pydockerreg /tmp/pydockerreg/pydockerreg

RUN cd /tmp/pydockerreg && python setup.py install

ENTRYPOINT ["pydr"]


