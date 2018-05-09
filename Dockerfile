# use this image to run multiple service
# add service in supervisord.conf

FROM ilemonrain/centos-sshd:6.9

MAINTAINER dachuichui <quanning@gmail.com>

COPY ./script /root/script/

RUN (localedef -v -c -i en_US -f UTF-8 en_US.UTF-8;\
    yum install -y supervisor crontabs gcc libnet libpcap;\

    mkdir -p /var/run/sshd;\
    mkdir -p /var/log/supervisor;\
    cp /root/script/supervisord.conf /etc/supervisord.conf;\

    chmod +x /root/script/supervisord;\
    chmod +x /root/script/net-speeder-master/net_speeder;\
    cp /root/script/supervisord /usr/bin/supervisord;\

    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime; \
    sed -i '/session    required   pam_loginuid.so/c\#session    required   pam_loginuid.so' /etc/pam.d/crond; \
    echo "*/3 * * * * /usr/bin/python /root/script/update.py >> /root/update.log 2>&1 &" >> /var/spool/cron/root; \

    cd /root/script/libsodium && make install; \
    ldconfig; \
    rm -rf /root/script/libsodium; \

    yum clean all;\
    rm -rf /var/cache/yum)

EXPOSE 22

ENTRYPOINT ["/usr/bin/supervisord"]
