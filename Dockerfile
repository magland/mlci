FROM magland/pynode:try1

RUN npm install -g @magland/kbucket

RUN pip3 install pandas numpy

RUN npm install -g yarn

# Install miniconda to /miniconda
RUN curl -LO http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
RUN bash Miniconda-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda

RUN pip install --upgrade yolk3k

ADD . /webapp
WORKDIR /webapp

CMD ./start.sh

