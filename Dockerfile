# use this image to run multiple service
# add service in supervisord.conf

FROM ilemonrain/centos-sshd:latest

MAINTAINER quanning quanning@gmail.com

COPY ./script /root/script/

RUN (localedef -v -c -i en_US -f UTF-8 en_US.UTF-8;\
    yum install -y supervisor gcc;\

    mkdir -p /var/run/sshd;\
    mkdir -p /var/log/supervisor;\
    cp /root/script/supervisord.conf /etc/supervisord.conf;\

    chmod +x /root/script/supervisord;\
    cp /root/script/supervisord /usr/bin/supervisord;\
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime;\

    cd /root/script/libsodium && make install; \
    ldconfig; \
    rm -rf /root/script/libsodium; \

    yum clean all;\
    rm -rf /var/cache/yum)

EXPOSE 22

ENTRYPOINT ["/usr/bin/supervisord"]
