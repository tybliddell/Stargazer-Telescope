FROM gocv/opencv:4.6.0
FROM debian:bullseye-20190708-slim
RUN apt-get update && apt-get install -y curl git jq
ARG TOKEN='REDACTED'
ARG REPO='https://api.github.com/repos/MRHT-SRProject/CamCtrl/releases/latest'
COPY --from=0 /usr/local/include/ /usr/local/include/
COPY --from=0 /usr/local/lib /usr/local/lib
RUN mv /usr/local/include/opencv4/opencv2/ /usr/local/include/opencv2/
RUN  mkdir /opt/camctrl && \ 
    curl -H "Authorization: token ${TOKEN}" -sL $(curl -H "Authorization: token ${TOKEN}" \
    -sL ${REPO} \
    | jq -r '.tarball_url') \
    | tar --strip-components=1 -xzC /opt/camctrl



FROM golang:1.19.1-bullseye
COPY --from=1 /opt/camctrl /opt/camctrl
COPY --from=1 /usr/local/ /usr/local/
WORKDIR /opt/camctrl
RUN apt-get update && apt-get install -y libraw-dev libtbb-dev libpng-dev libtiff-dev && \ 
    chmod +x build.sh && ./build.sh
ENTRYPOINT [ "bin/camctrl" ]