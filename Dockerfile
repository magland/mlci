FROM continuumio/miniconda3:latest

RUN conda install python=3.6
RUN conda install nodejs=8.11
RUN conda install pandas numpy

RUN pip install --upgrade yolk3k
RUN pip install setuptools

RUN npm install -g yarn

RUN conda install -c flatiron -c conda-forge kbucket


ADD . /webapp
WORKDIR /webapp

CMD ./start.sh

