FROM python:3.10-bullseye

RUN apt-get update && pip install --upgrade pip

# Download requirements files only
RUN curl --remote-name --location --request GET 'https://api.github.com/repos/MRHT-SRProject/AlpacaServer/contents/requirements.txt' \
--header 'Authorization: token REDACTED' \
--header 'Accept: application/vnd.github.v3.raw'

# Remove self hosted files eventually
RUN pip install -r requirements.txt --extra-index-url https://my.eng.utah.edu/~u1175601/ --only-binary=:all:

RUN curl --remote-name --location --request GET 'https://api.github.com/repos/MRHT-SRProject/StargazerServer-AlpacaClient/contents/requirements.txt' \
--header 'Authorization: token REDACTED' \
--header 'Accept: application/vnd.github.v3.raw'

# Remove self hosted files eventually
RUN pip install -r requirements.txt --extra-index-url https://my.eng.utah.edu/~u1175601/ --only-binary=:all:

RUN mkdir /opt/stargazer
RUN mkdir /opt/stargazer/repos
RUN mkdir /opt/stargazer/logs
WORKDIR "/opt/stargazer/repos"

# Clone repos using repo key
ADD https://REDACTED:x-oauth-basic@api.github.com/repos/MRHT-SRProject/StargazerServer-AlpacaClient/git/ref/heads/main /dev/null
RUN git clone https://REDACTED@github.com/MRHT-SRProject/StargazerServer-AlpacaClient
ADD https://REDACTED:x-oauth-basic@api.github.com/repos/MRHT-SRProject/AlpacaServer/git/ref/heads/main /dev/null
RUN git clone https://REDACTED@github.com/MRHT-SRProject/AlpacaServer

WORKDIR "/opt/stargazer"
ADD https://REDACTED:x-oauth-basic@api.github.com/repos/MRHT-SRProject/StargazerSetup/git/ref/heads/main /dev/null
RUN git clone https://REDACTED@github.com/MRHT-SRProject/StargazerSetup
RUN mkdir -p /opt/stargazer/StargazerSetup/logs
RUN chmod +x StargazerSetup/stargazer/start_stargazer.sh

ENTRYPOINT "StargazerSetup/stargazer/start_stargazer.sh"
