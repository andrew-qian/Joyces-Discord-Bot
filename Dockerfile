ARG CACHEBUST=1
FROM ubuntu:23.04
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
ARG DISCORD_TOKEN
ARG DISCORD_GUILD
RUN apt-get update 
RUN apt-get install -y python3 python3-pip git wget python3.11-venv
ARG CHROME_VERSION="109.0.5414.119-1"
RUN wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb \
  && apt install -y /tmp/chrome.deb \
  && rm /tmp/chrome.deb
RUN git clone https://github.com/andrew-qian/Joyces-Discord-Bot.git
WORKDIR "/Joyces-Discord-Bot"
RUN ls
RUN chmod a+x chromedriver

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
RUN source $VIRTUAL_ENV/bin/activate
RUN pip install -r requirements.txt
CMD ["python", "bot.py"]