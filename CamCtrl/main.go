package main

import (
	"fmt"
	"log"
	"os"
	"time"

	"github.com/MRHT-SRProject/camcapture/camera"
	"github.com/MRHT-SRProject/camcapture/comms"
	"github.com/MRHT-SRProject/camcapture/fsm"
	limage "github.com/MRHT-SRProject/camcapture/image"
	"github.com/MRHT-SRProject/go-img-processor/processors"
	"github.com/go-redis/redis/v8"
	"github.com/google/uuid"
)																									

type Quality string

const (
	GREAT   Quality = "HIGHEST"
	GOOD    Quality = "HIGH"
	OKAY    Quality = "OKAY"
	POOR    Quality = "POOR"
	TESTING Quality = "__TEST__"
)

var status fsm.Status
var cam camera.Camera
var compressed_image []byte

func main() {
	redis_url := "redis:6379"
	fmt.Fprint(os.Stderr, "CamCtrl started"+"\n")
	_, skip_cam_connect := os.LookupEnv("SKIP_CAM_CONNECT")
	if _, debug := os.LookupEnv("DEBUG"); debug {
		comms.SendMessage(comms.NOTICE, "Status DEBUG on")
		status.Debug = debug
	}
	if redis, redis_set := os.LookupEnv("REDIS_URL"); redis_set {
		redis_url = redis
	}
	comms.CreateClient(redis.Options{
		Addr:     redis_url,
		Password: "",
		DB:       0,
	})
	status.SetStatus(fsm.CONNECTING)
	cam = camera.Camera{}
	if connected, err := comms.VerifyConnect(); !connected {
		log.Fatal("Could not connect to Redis server: ", err.Error())
	}
	comms.SendMessage(comms.NOTICE, "Camera is listening to the ALPACA channel and sending on CAMERA_DATA and CAMERA_LOG_*.")
	// if we cannot connect report and keep trying indefinitely
	for {
		if skip_cam_connect {
			status.SetStatus(fsm.DISCONNECTED)
			comms.SendMessage(comms.WARNING, "skipping camera connect check. Errors may occur")
			break
		}
		err := cam.Connect()
		if err == nil {
			break
		}
		status.SetStatus(fsm.ERROR)
		comms.SendMessage(comms.ERROR, "Failed to connect to camera. Error:", err.Error(), "Retrying in 20s")
		// sleep for 20s and try to connect again
		time.Sleep(time.Duration(20 * time.Second))
	}

	fmt.Fprint(os.Stderr, "Camera connected"+"\n")
	comms.SendMessage(comms.NOTICE, "Successfully connected to the camera.")
	comms.SendMessage(comms.NOTICE, "Waiting for messages from ALPACA client")
	status.SetStatus(fsm.READY)
	go imageLoop()
	go statusLoop()
	captureLoop()

}

func statusLoop() {
	ch := comms.Listen("ALPACA")
	for {
		msg, err := comms.DecodeMessage(<-ch)
		if err != nil {
			comms.SendMessage(comms.ERROR, "Failed to decode message! Error:", err.Error())
			continue
		}

		switch msg.Command {
		case comms.STATUS:
			comms.SendResponse(comms.Response{ID: msg.ID, Data: status.GetStatusString()})
		case comms.ABORT:
			if status.GetStatus() != fsm.CAPTURING {
				comms.SendMessage(comms.WARNING, "Unable to abort, status is not CAPTURE. Ignoring.")
				break
			}

			cam.Cancel()
			status.SetStatus(fsm.READY)
		default:
			continue
		}

	}
}

func captureLoop() {
	ch := comms.Listen("ALPACA")
	for {
		msg, err := comms.DecodeMessage(<-ch)
		if err != nil {
			// status loop already reports the error
			continue
		}
		if msg.Command != comms.CAPTURE {
			continue
		}
		comms.SendMessage(comms.NOTICE, "Received message:", msg.String())
		status.SetStatus(fsm.CAPTURING)
		comms.SendMessage(comms.NOTICE, "Processing Capture Request.")
		comms.SendResponse(comms.Response{ID: msg.ID, Data: "Processing Request"})
		_light := msg.Args["light"]
		_time := msg.Args["time"]

		// TODO: Handle light frames
		_, ok := _light.(bool)
		t, ook := _time.(float64)

		if !(ok && ook) {
			comms.SendMessage(comms.ERROR, "Failed to parse args for capture request. Both light: bool and time: float32 must be provided as args.")
			continue
		}

		raw, err := cam.Capture(camera.ImgDef{Time: float32(t), Unit: "s"})
		if err != nil {
			comms.SendMessage(comms.ERROR, "Error Capturing Image:", err.Error())
			continue
		}

		comms.SendMessage(comms.NOTICE, "Decoding Image")
		img, _, err := processors.GetImageFromRaw(raw)
		if err != nil {
			comms.SendMessage(comms.ERROR, "Error Decoding Image:", err.Error())
		}
	
		comms.SendMessage(comms.NOTICE, "Compressing image")
		compressed_image, err = limage.Compress(img)
		if err != nil {
			comms.SendMessage("Error compressing image: ", err.Error())
			status.SetStatus(fsm.ERROR)
		}
		comms.SendMessage(comms.NOTICE, "Capture Completed Okay.")
		status.SetStatus(fsm.IMAGE_READY)
	}

}

func imageLoop() {
	ch := comms.Listen("ALPACA")
	for {
		msg, err := comms.DecodeMessage(<-ch)
		if err != nil {
			// status loop already reports the error
			continue
		}

		if msg.Command != comms.IMAGE {
			// only handle the image request
			continue
		}
		id := uuid.NewString()
		comms.SaveData(id, compressed_image)
		comms.SendResponse(comms.Response{ID: msg.ID, Data: id})
		comms.SendMessage(comms.NOTICE, "Capture Completed Okay.")
	}
}
