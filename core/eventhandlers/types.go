package eventhandlers

import (
	"github.com/pluyckx/kam/config"
)

type event int32

const (
	Event_Inactive        event = iota
	Event_InactiveTimeout event = iota
	Event_Active          event = iota
)

type EventHandler interface {
	LoadConfig(config *config.TomlSection) bool
	Handle(event event) error
}
