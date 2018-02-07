package eventhandlers

import (
	"github.com/pluyckx/kam/config"
	"github.com/pluyckx/kam/logging"
)

type InactiveTimeoutCommand struct {
	EventHandler

	cmd string
}

func (handler *InactiveTimeoutCommand) LoadConfig(config *config.TomlSection) bool {
	const sectionKey = "InactiveTimeout"
	const handlerKey = "handler"
	const handlerValue = "Command"
	const commandKey = "command"

	logger := logging.GetLogger("")

	logger.Debug("Loading section '%s'", sectionKey)
	section := config.Section(sectionKey)

	if section != nil {
		logger.Debug("Loading handler type")
		sHandler, ok := section.GetString(handlerKey)

		if ok && (sHandler == handlerValue) {
			logger.Debug("Loading command")
			cmd, ok := section.GetString(commandKey)

			if ok {
				logger.Debug("Command loaded: '%s'", cmd)
				handler.cmd = cmd

				return true
			} else {
				logger.Debug("No command found")
				return false
			}
		} else {
			if ok {
				logger.Debug("Expected handler '%s', but '%s' found", handlerValue, sHandler)
			} else {
				logger.Debug("No handler found")
			}
			return false
		}
	} else {
		logger.Debug("Section not found")
		return false
	}
}

func (handler *InactiveTimeoutCommand) Handle(event event) bool {
	return false
}
