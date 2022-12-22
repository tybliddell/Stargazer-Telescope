package image

import (
	"bytes"
	"encoding/gob"
	"image"
)

func Compress(img image.Image) ([]byte, error) {
	raw := bytes.NewBuffer(make([]byte, 0))
	enc := gob.NewEncoder(raw)
	err := enc.Encode(img)
	if err != nil {
		return nil, err
	}

	return raw.Bytes(), nil

}
