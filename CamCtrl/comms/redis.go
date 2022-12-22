package comms

import (
	"context"
	"encoding/json"
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

func SendResponse(response Response, save_db ...bool) {

	r, err := json.Marshal(&response) 
	if err != nil {
		SendMessage(ERROR, "Failed to encode response! Error:", err.Error())
		return
	}
	if len(save_db) > 0 {
		SaveData("TEST_R", r)
	}
	send("CAMERA_DATA", r)
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
	client.Append(context.TODO(), key, string(data))
}

func init() {
	_, debug = os.LookupEnv("DEBUG")
}
