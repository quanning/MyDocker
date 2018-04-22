# use this image to run multiple service
# add service in supervisord.conf

FROM centos:6.9

MAINTAINER quanning@gmail.com

COPY ./script /root/script/

RUN (localedef -v -c -i en_US -f UTF-8 en_US.UTF-8; \
    yum update -y; \
    yum install -y openssh-server initscripts epel-release wget passwd tar unzip supervisor gcc; \

    sed -i 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config; \
    sed -i 's/#UsePAM no/UsePAM no/g' /etc/ssh/sshd_config; \
    sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/' /etc/ssh/sshd_config; \

    mkdir -p /root/.ssh/; \
    echo "StrictHostKeyChecking=no" > /root/.ssh/config; \
    echo "UserKnownHostsFile=/dev/null" >> /root/.ssh/config; \

    /etc/init.d/sshd start; \
    sed -i 's/enabled=0/enabled=1/' /etc/yum.repos.d/CentOS-Base.repo; \
    echo "root:centos" | chpasswd ; \

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
