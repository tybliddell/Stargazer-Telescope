package db

import (
	"bytes"
	"encoding/gob"
	"image"
	redis "github.com/go-redis/redis/v8"
)

var client *redis.Client = redis.NewClient(&redis.Options{
	Addr:     "redis:6379",
	Password: "",
	DB:       0,
})

func GetSetMembers(key ...string) []string {
	imgs := make([]string, len(key))
	for i, k := range key {
		imgs[i] = client.Get(client.Context(), k).Val()
	}

	return imgs
}

func AddSetMembers(key string, members ...interface{}) {
	client.SAdd(client.Context(), key, members...)
}

func GetSetDiff(fromKey string, subKeys ...string) []string {
	keys := append([]string{fromKey}, subKeys...)
	return client.SDiff(client.Context(), keys...).Val()
}

func GetImages(key ...string) ([]image.Image, error) {
	gob.Register(image.RGBA{})
	imgBytes := GetSetMembers(key...)
	imgs := make([]image.Image, len(imgBytes))
	for i, strImg := range imgBytes {
		buf := bytes.NewBuffer([]byte(strImg))
		dec := gob.NewDecoder(buf)
		img := image.RGBA{}
		dec.Decode(&img)
		imgs[i] = &img
	}

	return imgs, nil
}

func AddKey(key string, value []byte) {
	client.Append(client.Context(), key, string(value))
}
