package schedulers

import (
	"math"
	"time"

	"github.com/pluyckx/kam/config"
	"github.com/pluyckx/kam/core/plugins"
	"github.com/pluyckx/kam/logging"
)

type Batch struct {
	pluginManager *plugins.Manager

	interval  uint32
	lastCycle time.Time
}

func (batch *Batch) SetPluginManager(manager *plugins.Manager) {
	batch.pluginManager = manager
}

func (batch *Batch) DoCycle() {
	logger := logging.GetLogger("")

	delay := batch.lastCycle.Sub(time.Now())
	delay += time.Duration(batch.interval) * time.Second

	logger.Info("Sleeping for %f seconds", math.Floor(float64(delay)+0.5))
	time.Sleep(delay)

	batch.lastCycle = time.Now()
	for _, plugin := range batch.pluginManager.GetPlugins() {
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
