package main

import (
	"github.com/pluyckx/kam/core/plugins"
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

	pluginsSection := config.Section("plugins")

	if pluginsSection == nil {
		panic("No plugins section found")
	}

	p := plugins.PsutilsCpu{}

	if !p.LoadConfig(pluginsSection) {
		logger.Error("Failed to load config file")
	}

	p.DoWork()
}
