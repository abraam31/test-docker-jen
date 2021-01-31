FROM ubuntu:18.04
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt-get update -y
RUN apt-get install -y wget
RUN apt install -y build-essential

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 
RUN conda --version
RUN apt-get install -y libmysqlclient-dev


EXPOSE 8000

WORKDIR /usr/src/app

COPY . ./

RUN conda create -n myenv python
RUN conda install -c anaconda django 
RUN pip install -r requirements.txt

ENTRYPOINT ["conda", "run", "-n", "myenv", "python", "manage.py", "runserver"]
