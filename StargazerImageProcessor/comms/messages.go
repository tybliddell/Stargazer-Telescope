package comms

import (
	"encoding/json"

	"github.com/go-redis/redis/v8"
)

type Command string

const (
	PROCESS Command = "PROCESS_IMAGE"
)

type Message struct {
	Command Command                `json:"command"`
	Args    map[string]interface{} `json:"args"`
	ID      string                 `json:"id,omitempty"`
}

type Response struct {
	ID   string `json:"id"`
	Data string `json:"data"`
	Status string `json:"status"`
}

func EncodeResponse(r *Response) ([]byte, error) {
	return json.Marshal(r)
}

func DecodeMessage(msg *redis.Message) (Message, error) {
	m := Message{}
	err := json.Unmarshal([]byte(msg.Payload), &m)
	return m, err
}

func (msg *Message) String() string {
	b, err := json.Marshal(msg)
	if err != nil {
		return "{}"
	}

	return string(b)
}
