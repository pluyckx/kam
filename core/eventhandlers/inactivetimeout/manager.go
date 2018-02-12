package inactivetimeout

import (
	"github.com/pluyckx/kam/config"
	"github.com/pluyckx/kam/core/eventhandlers"
	"github.com/pluyckx/kam/logging"
)

type Manager struct {
	handlers []eventhandlers.EventHandler

	dieOnInactive bool
}

func (manager *Manager) Add(handler eventhandlers.EventHandler) {
	manager.handlers = append(manager.handlers, handler)
}

func (manager *Manager) HandleEvent(event eventhandlers.Event) bool {
	for _, handler := range manager.handlers {
		handler.Handle(event)
	}

	return manager.dieOnInactive
}

func (manager *Manager) LoadConfig(config *config.TomlSection) bool {
	const sectionKey = "inactivetimeout"
	const dieOnInactiveKey = "die_on_inactive"

	logger := logging.GetLogger("")

	logger.Debug("Loading section '%s'", sectionKey)
	section := config.Section(sectionKey)

	if section == nil {
		logger.Warning("Section '%s' not found", sectionKey)
		return false
	}

	value, ok := section.GetBool(dieOnInactiveKey)

	if !ok {
		logger.Warning("Parameter '%s' invalid", dieOnInactiveKey)
		return false
	}

	manager.dieOnInactive = value

	return true
}

func (manager *Manager) logConfig() {
	logger := logging.GetLogger("")

	if logger != nil {
		logger.Info("eventhandlers.inactivetimeout config: die_on_inactive=%t", manager.dieOnInactive)
	}
}
