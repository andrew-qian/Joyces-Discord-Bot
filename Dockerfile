FROM ubuntu:23.04
ARG CACHEBUST=1
ARG DISCORD_TOKEN
ARG DISCORD_GUILD
RUN apt-get update 
RUN apt-get install -y python3 python3-pip
RUN apt -f install -y
RUN apt-get install -y wget
ARG CHROME_VERSION="109.0.5414.119-1"
RUN wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb \
  && apt install -y /tmp/chrome.deb \
  && rm /tmp/chrome.deb
RUN apt-get install -y git
RUN git clone https://github.com/andrew-qian/Joyces-Discord-Bot.git
WORKDIR "/Joyces-Discord-Bot"
RUN ls
RUN chmod a+x chromedriver
RUN pip install -r requirements.txt
CMD [ "python3", "-u", "bot.py" ]