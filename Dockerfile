FROM amazonlinux:latest

USER root

RUN yum install -y python-setuptools
RUN easy_install supervisor
RUN yum install -y git wget unzip python3 python3-pip
########## Setup google chrome ###########
##########################################
RUN cd /tmp/    
RUN wget https://chromedriver.storage.googleapis.com/100.0.4896.20/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/bin/chromedriver

RUN curl https://intoli.com/install-google-chrome.sh | bash
RUN mv /usr/bin/google-chrome-stable /usr/bin/google-chrome

#RUN amazon-linux-extras install python3

########## Setup application #############
##########################################
WORKDIR /root/newsfeed

COPY . .

RUN pip3 install -r requirements.txt --upgrade
########## Setup supervisor ##############
##########################################
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY configs/conf.d/* /etc/supervisor/conf.d/
RUN touch /var/run/supervisor.sock
RUN chmod 777 /var/run/supervisor.sock
##########################################
##########################################

ENV PYTHONPATH /root/newsfeed:$PYTHONPATH

EXPOSE 5000

ENTRYPOINT /usr/bin/supervisord

#ENTRYPOINT ["python3", "app/core/bot.py"]

