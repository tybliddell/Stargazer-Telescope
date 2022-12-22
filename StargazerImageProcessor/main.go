package main

import (
	"bytes"
	"fmt"
	"image"
	"image/jpeg"
	"log"
	"math/rand"
	"os"
	"time"

	"github.com/MRHT-SRProject/go-img-processor/processors"
	"github.com/MRHT-SRProject/stargazer-image-processor/comms"
	"github.com/MRHT-SRProject/stargazer-image-processor/db"
)

var imgInProcess image.Image

func main() {
	// non-deterministic random source
	r := rand.New(rand.NewSource(time.Now().Unix()))
	ch := comms.Listen("IMAGE_PROCESSOR_COMMAND")
	for {
		msg, ok := <-ch
		if !ok {
			log.Println("Failed to open channel")
		}
		message, err := comms.DecodeMessage(msg)
		if err != nil {
			handleError(err, message.ID, "Error decoding message")
			continue
		}
		arg_keys := message.Args["db_keys"].([]interface{})
		keys := make([]string, len(arg_keys))
		for i, k := range arg_keys {
			keys[i] = k.(string)
		}
		fmt.Fprintln(os.Stderr, "Received image process request")
		if message.Command == comms.PROCESS {
			imgs, err := db.GetImages(keys...)
			if err != nil {
				handleError(err, message.ID, "Error getting images")
			}

			if imgInProcess != nil {
				imgs = append(imgs, imgInProcess)
			}
			fmt.Fprintln(os.Stderr, "Beginning Process")
			gsImgs, err := processors.GrayScale(imgs...)
			if err != nil {
				handleError(err, message.ID, "CV error converting images to grayscale")
				continue
			}
			fmt.Fprintln(os.Stderr, "Converted images to grayscale")
			fmt.Fprintln(os.Stderr, "Stacking images")
			stacked, err := processors.StackImages(gsImgs...)
			if err != nil {
				handleError(err, message.ID, "CV error stacking images")
				continue
			}
			fmt.Fprintln(os.Stderr, "Images stacked")
			fmt.Fprintln(os.Stderr, "Colorizing image")
			var processed processors.CMat
			color := (processors.ColormapTypes)(r.Intn(22))
			processed, err = processors.Colorize(stacked, color)
			if err != nil {
				log.Println("CV error colorizing image. Returning grayscale image instead")
				log.Println("Error: ", err.Error())
				processed = stacked
			}
			fmt.Fprintln(os.Stderr, "Image colorized")
			log.Println("Converting bytes to image")
			img, err := processors.CMatToImg(processed)
			if err != nil {
				handleError(err, message.ID, "Error converting CMat to Image")
				continue;
			}
			fmt.Fprintln(os.Stderr, "Converting image to jpg")
			if err != nil {
				handleError(err, message.ID, "Error converting Image to jpg")
				continue;
			}
			jpg := bytes.NewBuffer(make([]byte, 0))
			jpeg.Encode(jpg, img, &jpeg.Options{
				Quality: 100,
			})
			fmt.Fprintln(os.Stderr, "Image process complete")
			key := fmt.Sprintf("%s.jpg", message.ID)
			db.AddKey(key, jpg.Bytes())
			comms.SendResponse(comms.Response{
				ID:     message.ID,
				Data:   key,
				Status: "ok",
			})
		}
	}

}

func handleError(err error, id string, msg ...any) {
	msg = append(msg, "ERROR: ", err.Error())
	log.Println(msg...)
	comms.SendResponse(comms.Response{ID: id, Status: "error", Data: err.Error()})
}
