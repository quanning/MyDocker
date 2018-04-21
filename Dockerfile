# use this image to run multiple service
# add service in supervisord.conf

FROM ilemonrain/centos-sshd:latest

MAINTAINER quanning@gmail.com

COPY ./script /root/script/

RUN (localedef -v -c -i en_US -f UTF-8 en_US.UTF-8;\
    yum install -y supervisor crontabs;\

    mkdir -p /var/run/sshd;\
    mkdir -p /var/log/supervisor;\
    cp /root/script/supervisord.conf /etc/supervisord.conf;\

    chmod +x /root/script/getip.py;\
    chmod +x /root/script/supervisord;\
    cp /root/script/supervisord /usr/bin/supervisord;\

    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime;\
    sed -i '/session    required   pam_loginuid.so/c\#session    required   pam_loginuid.so' /etc/pam.d/crond;\
    echo "*/1 * * * * /bin/echo 'it works.' >> /root/test.log" >> /var/spool/cron/root;\
    echo "*/1 * * * * /usr/bin/python /root/script/getip.py >> /root/getip.log 2>&1 &" >> /var/spool/cron/root;\

    yum clean all;\
    rm -rf /var/cache/yum)

EXPOSE 22

ENTRYPOINT ["/usr/bin/supervisord"]
