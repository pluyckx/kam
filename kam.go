package main

import (
	"time"

	"github.com/pluyckx/kam/core/eventhandlers"

	"github.com/pluyckx/kam/core/eventhandlers/inactivetimeout"
	"github.com/pluyckx/kam/core/plugins"
	"github.com/pluyckx/kam/core/schedulers"
	"github.com/pluyckx/kam/logging"

	"github.com/pluyckx/kam/config"
)

func main() {
	logger, err := logging.NewFileLogger("/tmp/kam.log")

	if err != nil {
		panic(err)
	}

	logger.SetLevel(logging.Level_Debug)

	ok := logging.RegisterLogger("", logger)

	if !ok {
		panic("Could not register logger")
	}

	config, err := config.LoadFile("config.toml")

	if err != nil {
		panic(err)
	}

	scheduler := schedulers.Batch{}
	scheduler.LoadConfig(config.Section("scheduler"))

	pluginsManager := plugins.Manager{}
	pluginsManager.LoadPlugins(config)

	inactiveTimeoutManager := inactivetimeout.Manager{}
	inactiveTimeoutManager.LoadConfig(config.Section("eventhandler"))
	inactiveTimeoutManager.LoadHandlers(config.Section("eventhandler"))

	scheduler.SetPluginManager(&pluginsManager)

	lastActive := time.Now()
	isInactive := false

	for (!inactiveTimeoutManager.DieOnInactive()) || (!inactiveTimeoutManager.IsInactive(lastActive)) {
		scheduler.DoCycle()

		if pluginsManager.HasActive() {
			logger.Info("Device is alive")
			lastActive = time.Now()
			isInactive = false
		} else {
			logger.Info("Device is inactive for %f", float64(time.Since(lastActive)))

			if inactiveTimeoutManager.IsInactive(lastActive) {

				if !isInactive {
					inactiveTimeoutManager.HandleEvent(eventhandlers.Event_InactiveTimeout)
				}

				isInactive = true
			}
		}
	}
}
