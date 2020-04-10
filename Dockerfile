FROM ubuntu:18.04
RUN apt-get update
RUN apt-get -y --no-install-recommends install gnupg
RUN apt-key adv --keyserver pool.sks-keyservers.net --recv 1078ECD7
RUN echo "deb http://apt.arvados.org/ bionic main" | tee /etc/apt/sources.list.d/arvados.list
RUN apt-get update
RUN apt-get install -y arvados-api-server arvados-controller ruby-bundler nginx ruby-dev
