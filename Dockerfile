FROM python:3.10-slim

#recommended when running python in docker
ENV PYTHONUNBUFFERED 1

LABEL maintainer="Michael Lee" \
      version="1.0" \
      description="dockerfile for group3_package's api"

# Set the container's working directory to /app
RUN mkdir /app
WORKDIR /app

# copy the contents of the current dir into /app inside the container
COPY . /app

# gcc is required for biopython, a python package from BLAST to install
RUN apt-get update && apt-get install -y gcc


# make sure our python package is installed
RUN pip install -e group3_package/