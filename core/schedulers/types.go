package schedulers

import (
	"github.com/pluyckx/kam/config"
	"github.com/pluyckx/kam/core/plugins"
)

type Scheduler interface {
	LoadConfig(config *config.TomlSection) bool
	AddPlugin(plugin *plugins.Plugin)
	DoCycle()
	HasActivePlugin() bool
}
