FROM pasmod/miniconder2

RUN apt-get update && \
	apt-get install -y build-essential libxml2-dev libxslt-dev libsm6 libxrender1 libfontconfig1 libicu-dev python-dev python-openssl && \
  apt-get install -y libblas-dev liblapack-dev libatlas-base-dev gfortran && \
	apt-get clean
RUN apt-get install -y python-pip python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev libjpeg8-dev zlib1g-dev

RUN conda install -y \
  beautifulsoup4==4.4.1

RUN pip install redis
RUN pip install unidecode
RUN pip install numpy
RUN pip install --upgrade cython
RUN pip install lxml
RUN pip install dragnet
RUN pip install httplib2
RUN pip install gunicorn

WORKDIR /var/www
ADD . .
RUN mkdir piplib
RUN pip install --upgrade pip
RUN pip install -r requirements.txt -t piplib
