package inactivetimeout

import (
	"time"

	"github.com/pluyckx/kam/config"
	"github.com/pluyckx/kam/core/eventhandlers"
	"github.com/pluyckx/kam/logging"
)

type Manager struct {
	handlers []eventhandlers.EventHandler

	dieOnInactive   bool
	inactiveTimeout int32
}

func (manager *Manager) Add(handler eventhandlers.EventHandler) {
	manager.handlers = append(manager.handlers, handler)
}

func (manager *Manager) HandleEvent(event eventhandlers.Event) bool {
	if event == eventhandlers.Event_InactiveTimeout {
		for _, handler := range manager.handlers {
			handler.Handle(event)
		}
	}

	return manager.dieOnInactive
}

func (manager *Manager) IsInactive(lastActivity time.Time) bool {
	duration := time.Since(lastActivity)

	return duration.Seconds() >= float64(manager.inactiveTimeout)
}

func (manager *Manager) DieOnInactive() bool {
	return manager.dieOnInactive
}

func (manager *Manager) LoadHandlers(config *config.TomlSection) bool {
	const sectionKey = "inactivetimeout"

	logger := logging.GetLogger("")

	section := config.Section(sectionKey)

	if section == nil {
		logger.Error("Section '%' not found", sectionKey)
	}

	var handler eventhandlers.EventHandler = &InactiveTimeoutCommand{}

	if handler.LoadConfig(config) {
		manager.Add(handler)
	}

	return true
}

func (manager *Manager) LoadConfig(config *config.TomlSection) bool {
	const sectionKey = "inactivetimeout"
	const dieOnInactiveKey = "die_on_inactive"
	const inactiveTimeoutParameter = "inactive_timeout"

	logger := logging.GetLogger("")

	logger.Debug("Loading section '%s'", sectionKey)
	section := config.Section(sectionKey)

	manager.dieOnInactive = false
	manager.inactiveTimeout = 1800

	if section == nil {
		logger.Warning("Section '%s' not found", sectionKey)
		return false
	}

	var ok bool

	manager.dieOnInactive, ok = section.GetBool(dieOnInactiveKey)

	if !ok {
		logger.Warning("Parameter '%s' invalid", dieOnInactiveKey)
		return false
	}

	i64, ok := section.GetInteger(inactiveTimeoutParameter)
	manager.inactiveTimeout = int32(i64)

	if !ok {
		logger.Warning("Parameter '%s' invalid", inactiveTimeoutParameter)
		return false
	}

	return true
}

func (manager *Manager) logConfig() {
	logger := logging.GetLogger("")

	if logger != nil {
		logger.Info("eventhandlers.inactivetimeout config: die_on_inactive=%t", manager.dieOnInactive)
	}
}
