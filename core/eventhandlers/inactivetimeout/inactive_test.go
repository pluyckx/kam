package inactivetimeout

import (
	"os"
	"testing"

	"github.com/pluyckx/kam/logging"

	"github.com/pluyckx/kam/config"
)

const enableLogger = true

const inactiveFullConfig = `
[eventhandler]

	[eventhandler.inactivetimeout]

		[eventhandler.inactivetimeout.command]
			command = "echo"
			parameters = ["Computer", "is idle"]
`

const eventhandlerKey = "eventhandler"
const inactiveTimeoutKey = "inactivetimeout"
const commandKey = "command"

func TestLoadFullConfig(t *testing.T) {
	if enableLogger {
		logging.RegisterLogger("", logging.NewLogger(os.Stdout))
		logging.GetLogger("").SetLevel(logging.Level_Debug)
	}

	cfg, err := config.LoadData(inactiveFullConfig)

	if err != nil {
		t.Error("Invalid config")
		return
	}

	cfg = cfg.Section("eventhandler")

	if cfg == nil {
		t.Error("eventhandler section not found")
		return
	}

	cmd := InactiveTimeoutCommand{}

	if !cmd.LoadConfig(cfg) {
		t.Error("Problems during loading config")
	}
}
