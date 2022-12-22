# CamCapture

## Flags

| **Flag**          |  **Definition**                                       |      **Defualt** |
|:------------------|:-----------------------------------------------------:|-----------------:|
| DEBUG             | Print all messages to STDERR as well as Redis         |   False          |
| SKIP_CAM_CONNECT  |  Bypass camera connection check. May result in errors |   False          |
| REDIS_URL         | The URL to use to connect to Redis                    |   localhost:6379 |

## Build

`$ ./build.sh`

## Run
`$ DEBUG=1 SKIP_CAM_CONNECT=0 REDIS_URL=redis:1234 ./bin/camctrl`