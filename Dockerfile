
FROM    ubuntu:14.04

RUN     sudo apt-get update

# Install node and npm
RUN     sudo apt-get install -y nodejs
RUN     sudo ln -sf /usr/bin/nodejs /usr/local/bin/node
RUN     sudo apt-get install -y npm
RUN     sudo apt-get install -y libpq-dev build-essential

# Install SSH daemon and set up supervisor
RUN     apt-get install -y openssh-server supervisor
RUN     mkdir -p /var/run/sshd
RUN     mkdir -p /var/log/supervisor
RUN     mkdir /root/.ssh/

# ADD <src> <dest>. <src> must be the path to a file or directory relative to the source directory being built
# These are the keys that allow us to ssh into the container.
ADD     econapp_docker_rsa.pub /tmp/econapp_docker_rsa.pub
RUN     cat /tmp/econapp_docker_rsa.pub >> /root/.ssh/authorized_keys && rm -f /tmp/econapp_docker_rsa.pub

ADD     ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Load and install the app
ADD     . /src
RUN     cd /src; npm install

# Expose node and ssh
EXPOSE  5000 22 8081

# Set the default command to run when starting the container
CMD     ["/usr/bin/supervisord"]