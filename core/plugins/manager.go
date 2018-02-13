package plugins

import (
	"github.com/pluyckx/kam/config"
	"github.com/pluyckx/kam/core/plugins/psutils"
	"github.com/pluyckx/kam/logging"
)

type Manager struct {
	plugins []Plugin
}

func (manager *Manager) Add(plugin Plugin) {
	manager.plugins = append(manager.plugins, plugin)
}

func (manager *Manager) HasActive() bool {
	active := false

	for _, plugin := range manager.plugins {
		if plugin.IsActive() {
			active = true

			break
		}
	}

	return active
}

func (manager *Manager) GetPlugins() []Plugin {
	return manager.plugins
}

func (manager *Manager) LoadPlugins(config *config.TomlSection) bool {
	const pluginsKey = "plugins"

	logger := logging.GetLogger("")
	pluginSection := config.Section(pluginsKey)

	if pluginSection == nil {
		logger.Error("No section '%s' found", pluginsKey)
	}

	var plugin Plugin = &psutils.PsutilsCpu{}

	if plugin.LoadConfig(pluginSection) {
		manager.Add(plugin)
	}

	return true
}
