FROM os/centos7
MAINTAINER laurent.licour@ext.adeo.com

RUN yum -y install httpd mod_ssl mod_wsgi python python-virtualenv gcc wget
RUN yum clean all

RUN mkdir -p /home3/beapi/log
RUN chown -R apache /home3/beapi
RUN mkdir -p /usr/local/beapi

WORKDIR /usr/local/beapi

COPY conf conf
COPY def def
COPY env env
COPY install install
COPY contrib contrib
COPY resources resources

RUN install/flaskit_mkvenv
RUN ln -sf /usr/local/beapi/env/beapi.default/httpd.conf /etc/httpd/conf.d/beapi.conf

CMD ["/usr/sbin/apachectl", "-D", "FOREGROUND"]
EXPOSE 8445
