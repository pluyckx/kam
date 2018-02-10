package eventhandlers

import (
	"os"
	"os/exec"

	"github.com/pluyckx/kam/config"
	"github.com/pluyckx/kam/logging"
)

type InactiveTimeoutCommand struct {
	EventHandler

	cmd        string
	parameters []string
}

func (handler *InactiveTimeoutCommand) LoadConfig(config *config.TomlSection) bool {
	const sectionInactiveTimeoutKey = "inactivetimeout"
	const sectionCommandKey = "command"
	const handlerKey = "handler"
	const handlerValue = "command"
	const commandKey = "command"
	const parameterKey = "parameters"

	logger := logging.GetLogger("")

	logger.Debug("Loading section '%s'", sectionInactiveTimeoutKey)
	section := config.Section(sectionInactiveTimeoutKey)

	if section == nil {
		logger.Warning("Section '%s' not found", sectionInactiveTimeoutKey)
		return false
	}

	logger.Debug("Loading section '%s' from '%s'", sectionCommandKey, sectionInactiveTimeoutKey)
	section = section.Section(sectionCommandKey)

	if section == nil {
		logger.Warning("No section '%s' found in '%s'", sectionCommandKey, sectionInactiveTimeoutKey)
		return false
	}

	logger.Debug("Loading command")
	cmd, ok := section.GetString(commandKey)

	if ok {
		logger.Debug("Command loaded: '%s'", cmd)
		handler.cmd = cmd

		logger.Debug("Loading parameter if available")
		parameters, ok := section.GetStringArray(parameterKey)

		if ok {
			logger.Info("Parameters found: %v", parameters)
			handler.parameters = parameters
		} else {
			logger.Info("No parameters available")
		}

		return true
	} else {
		logger.Debug("No command found")
		return false
	}
}

func (handler *InactiveTimeoutCommand) Handle(event event) error {
	if event == Event_InactiveTimeout {
		cmd := exec.Command(handler.cmd, handler.parameters...)

		cmd.Stdout = os.Stdout

		return cmd.Run()
	} else {
		return nil
	}
}
