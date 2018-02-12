package eventhandlers

import (
	"github.com/pluyckx/kam/config"
)

type Event int32

const (
	Event_Inactive        Event = iota
	Event_InactiveTimeout Event = iota
	Event_Active          Event = iota
)

type EventHandler interface {
	LoadConfig(config *config.TomlSection) bool
	Handle(event Event) error
}
