package main

import (
	"fmt"

	"github.com/pluyckx/kam/logging"

	"github.com/pluyckx/kam/config"
	"github.com/pluyckx/kam/core/eventhandlers"
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

	handler := eventhandlers.InactiveTimeoutCommand{}
	if handler.LoadConfig(config) {
		fmt.Println("Config loaded")

		err := handler.Handle(eventhandlers.Event_InactiveTimeout)

		if err != nil {
			panic(err)
		}
	} else {
		fmt.Println("Config load failed")
	}
}
