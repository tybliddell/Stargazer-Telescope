package comms

import (
	"encoding/json"

	"github.com/go-redis/redis/v8"
)

type Command string

const (
	CAPTURE Command = "CAPTURE"
	ABORT   Command = "ABORT"
	STATUS  Command = "STATUS"
	IMAGE   Command = "LAST_IMAGE"
)

type Message struct {
	Command Command                `json:"command"`
	Args    map[string]interface{} `json:"args"`
	ID      int                    `json:"id,omitempty"`
}

type Response struct {
	ID   int    `json:"id"`
	Data string `json:"data"`
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
