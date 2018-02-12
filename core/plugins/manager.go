package plugins

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
