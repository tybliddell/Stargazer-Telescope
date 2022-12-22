package main

import (
	"bytes"
	"encoding/base64"
	"encoding/gob"
	"image"
	"image/png"
	"log"
	"os"
)


func main() {
	f, err := os.Open("./test.png")
	handleError(11, err)
	img, err := png.Decode(f)
	handleError(13, err)
	imgGob := bytes.Buffer{}
	enc := gob.NewEncoder(&imgGob)
	enc.Encode(img)
	b64 := base64.RawStdEncoding.EncodeToString(imgGob.Bytes())
	out, err := os.Create("encoded.txt")
	handleError(22, err)
	out.Write([]byte(b64))
	out.Close()
	encoded, err := os.Open("./encoded.txt")
	handleError(26, err)
	info, _ := encoded.Stat()
	encodedBytes := make([]byte, info.Size())
	decoded := bytes.NewBuffer(make([]byte, info.Size()))
	encoded.Read(encodedBytes)
	_, err = base64.RawStdEncoding.Decode(decoded.Bytes(), encodedBytes)
	handleError(32, err)
	dec := gob.NewDecoder(decoded)
	restoredImage := image.RGBA{}
	err = dec.Decode(&restoredImage)
	handleError(37, err)
	restoredPng, err := os.Create("restored.png")
	handleError(39, err)
	png.Encode(restoredPng, &restoredImage)
	defer func ()  {
		f.Close()
		encoded.Close()
		restoredPng.Close()
	}()
}

func handleError(line int, err error) {
	if err != nil {
		log.Fatal("Fatal error line ", line, ": ", err.Error())
	}
}