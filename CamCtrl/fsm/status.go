package fsm

import "github.com/MRHT-SRProject/camcapture/comms"

type StatusVal string
type Status struct {
	Debug  bool
	status StatusVal
}

func (s *Status) GetStatus() StatusVal {
	if s.Debug {
		comms.SendMessage(comms.NOTICE, "Status Requested. Returning ", string(s.status))
	}
	return s.status
}

func (s *Status) SetStatus(status StatusVal) {
	if s.Debug {
		comms.SendMessage(comms.NOTICE, "Setting Status: ", string(s.status))
	}
	s.status = status
}

func (s *Status) GetStatusString() string {
	if s.Debug {
		comms.SendMessage(comms.NOTICE, "Status Requested. Returning ", string(s.status))
	}
	return string(s.status)
}

const (
	READY        StatusVal = "READY"
	PROCESSING   StatusVal = "PROCESSING"
	CAPTURING    StatusVal = "CAPTURING"
	ERROR        StatusVal = "ERROR"
	CONNECTING   StatusVal = "CONNECTING"
	DISCONNECTED StatusVal = "DISCONNECTED"
	IMAGE_READY  StatusVal = "IMAGE_READY"
)
