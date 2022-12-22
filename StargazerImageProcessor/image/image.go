package image

type ImageEncoding struct {
	Pix []byte `bson:"pix"`
	Dims struct {
		X int `bson:"x"`
		Y int `bson:"y"`
	}  `bson:"dims,inline"`
}