package plugins

import "github.com/pluyckx/kam/config"

type Plugin interface {
	LoadConfig(config *config.TomlSection) bool
	DoWork()
	IsActive() bool
}
