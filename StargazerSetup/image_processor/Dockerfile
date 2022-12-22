FROM richbai90/opencv:latest
FROM debian:bullseye-20190708-slim
RUN apt-get update && apt-get install -y curl git jq
ARG TOKEN='REDACTED'
ARG REPO='https://api.github.com/repos/MRHT-SRProject/stargazer-image-processor/releases/latest'
COPY --from=0 /usr/local/include/ /usr/local/include/
COPY --from=0 /usr/local/lib /usr/local/lib
RUN mv /usr/local/include/opencv4/opencv2/ /usr/local/include/opencv2/
# invalidate the cache
ARG COMMIT_HASH=
RUN  mkdir /opt/img_processor && \ 
    curl -H "Authorization: token ${TOKEN}" -sL $(curl -H "Authorization: token ${TOKEN}" \
    -sL ${REPO} \
    | jq -r '.tarball_url') \
    | tar --strip-components=1 -xzC /opt/img_processor



FROM golang:1.19.1-bullseye
COPY --from=1 /opt/img_processor /opt/img_processor
COPY --from=1 /usr/local/ /usr/local/
WORKDIR /opt/img_processor
RUN apt-get update && apt-get install -y libraw-dev libtbb-dev libpng-dev libtiff-dev gphoto2 && \ 
    chmod +x build.sh && ./build.sh
ENTRYPOINT [ "bin/image_processor" ]
