package schedulers

import (
	"github.com/pluyckx/kam/config"
	"github.com/pluyckx/kam/core/plugins"
	"github.com/pluyckx/kam/logging"
)

type Batch struct {
	plugins []plugins.Plugin

	interval uint32
}

func (batch *Batch) SetPlugins(plugins []plugins.Plugin) {
	batch.plugins = plugins
}

func (batch *Batch) DoCycle() {
	for _, plugin := range batch.plugins {
		plugin.DoWork()
	}
}

func (batch *Batch) LoadConfig(config *config.TomlSection) bool {
	const sectionBatchKey = "batch"
	const intervalKey = "interval"

	logger := logging.GetLogger("")

	logger.Debug("Loading section '%s'", sectionBatchKey)
	section := config.Section(sectionBatchKey)

	if section == nil {
		logger.Warning("Section '%s' not found", sectionBatchKey)
		return false
	}

	logger.Debug("Loading parameter '%s'", intervalKey)
	value, ok := section.GetInteger(intervalKey)

	if !ok {
		logger.Warning("Parameter '%s' not found", intervalKey)
		return false
	} else {
		batch.interval = uint32(value)
	}

	batch.logConfig()

	return true
}

func (batch *Batch) logConfig() {
	logger := logging.GetLogger("")

	if logger != nil {
		logger.Info("scheduler.batch config: interval=%d", batch.interval)
	}
}
