package comms

import (
	"context"
	"fmt"
	"os"
	"strings"
	redis "github.com/go-redis/redis/v8"
)

type LogLvl string

const (
	ERROR   LogLvl = "ERROR"
	NOTICE  LogLvl = "NOTICE"
	WARNING LogLvl = "WARNING"
)

var debug bool

var client *redis.Client = redis.NewClient(&redis.Options{
	Addr:     "redis:6379",
	Password: "",
	DB:       0,
})

func VerifyConnect() (bool, error) {
	status := client.Ping(context.TODO());
	return status.Err() == nil, status.Err()
}

func CreateClient(opts redis.Options) {
	client = redis.NewClient(&opts)

}

func SendMessage(lvl LogLvl, msg ...string) {
	fullMsg := strings.Join(msg, " ")
	if debug {
		fmt.Fprint(os.Stderr, fullMsg + "\n")
	}
	m := []byte(fullMsg)
	send("CAMERA_LOG_"+string(lvl), m)
}

func SendResponse(response Response) {
	r, err := EncodeResponse(&response)
	if err != nil {
		SendMessage(ERROR, "Failed to encode response! Error:", err.Error())
		return
	}
	send("IMAGE_PROCESSOR_FINISHED", r)
	SendMessage(NOTICE, "Camera Data Sent: ", string(r))
}

func send(ch string, msg []byte) {
	client.Publish(context.TODO(), ch, msg)
}

func Listen(channel string) <-chan *redis.Message {
	sub := client.Subscribe(context.TODO(), channel)
	return sub.Channel()
}

func SaveData(key string, data []byte) {
	client.SAdd(context.TODO(), key, data)
}

func init() {
	_, debug = os.LookupEnv("DEBUG")
}
