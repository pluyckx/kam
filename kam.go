package main

import (
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

	section := config.Section("scheduler")

	if section == nil {
		logger.Error("No scheduler section found")
	}

	batch := schedulers.Batch{}

	if !batch.LoadConfig(section) {
		logger.Error("Fault parsing config")
	}

	batch.DoCycle()
}
