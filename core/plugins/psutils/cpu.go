package psutils

import (
	"github.com/pluyckx/kam/config"
	"github.com/pluyckx/kam/logging"
	"github.com/shirou/gopsutil/cpu"
)

type PsutilsCpu struct {
	enabled bool
	active  bool

	total_threshold   float64
	per_cpu_threshold float64
}

func (psutilscpu *PsutilsCpu) IsActive() bool {
	return psutilscpu.active
}

func (psutilscpu *PsutilsCpu) DoWork() {
	logger := logging.GetLogger("")

	if !psutilscpu.enabled {
		logger.Debug("Not enabled")
		return
	}

	psutilscpu.active = false

	values, err := cpu.Percent(0, true)

	if err != nil {
		logger.Warning("%s", err)
		return
	}

	total := 0.0

	for _, v := range values {
		if v >= psutilscpu.per_cpu_threshold {
			psutilscpu.active = true

			logger.Info("Cpu usage: %f >= %f", v, psutilscpu.per_cpu_threshold)
		} else {
			logger.Debug("Cpu usage: %f < %f", v, psutilscpu.per_cpu_threshold)
		}

		total += v
	}

	if total >= psutilscpu.total_threshold {
		psutilscpu.active = true
		logger.Info("Total cpu usage: %f >= %f", total, psutilscpu.total_threshold)
	} else {
		logger.Debug("Total cpu usage: %f < %f", total, psutilscpu.total_threshold)
	}
}

func (psutilscpu *PsutilsCpu) LoadConfig(config *config.TomlSection) bool {
	const psutilsSectionKey = "psutil"
	const cpuSectionKey = "cpu"
	const enabledKey = "enabled"
	const totalThresholdKey = "total_cpu_threshold"
	const perCpuThresholdKey = "per_cpu_threshold"

	defer psutilscpu.logConfig()

	logger := logging.GetLogger("")

	cpuCount, err := cpu.Counts(true)

	if err != nil {
		logger.Error("%s", err)
	}

	logger.Debug("Loading global section '%s'", psutilsSectionKey)
	psutilsSection := config.Section(psutilsSectionKey)

	if psutilsSection == nil {
		return false
	}

	logger.Debug("Loading section '%s' from '%s'", cpuSectionKey, psutilsSectionKey)
	cpuSection := psutilsSection.Section(cpuSectionKey)

	if cpuSection == nil {
		return false
	}

	var ok bool

	psutilscpu.enabled, ok = cpuSection.GetBool(enabledKey)

	if !ok {
		logger.Debug("'%s' has no valid '%s' value. Plugin disabled.", cpuSectionKey, enabledKey)
	}

	logger.Debug("'%s' enabled = %t", cpuSectionKey, psutilscpu.enabled)

	if !psutilscpu.enabled {
		return true
	}

	tmp, ok := cpuSection.GetFloat(totalThresholdKey)

	if !ok {
		logger.Debug("'%s' not found or it contains an invalid value (float expected)", totalThresholdKey)
	} else {
		if tmp > 100.0 {
			logger.Debug("Too high value (%f) for '%s'. Max allowed is %f", tmp, totalThresholdKey, 100.0)
			psutilscpu.total_threshold = 0.0
		} else {
			psutilscpu.total_threshold = tmp * float64(cpuCount)
			logger.Debug("'%s' = %f, #cpu = %d --> %f used for %s", totalThresholdKey, tmp, cpuCount, psutilscpu.total_threshold, totalThresholdKey)
		}
	}

	psutilscpu.per_cpu_threshold, ok = cpuSection.GetFloat(perCpuThresholdKey)

	if !ok {
		logger.Debug("'%s' not found or it contains an invalid value (float expected)", perCpuThresholdKey)
	} else {
		if psutilscpu.per_cpu_threshold > 100.0 {
			logger.Debug("Too high value (%f) for '%s'. Max allowed is %f", psutilscpu.per_cpu_threshold, perCpuThresholdKey, 100.0)
			psutilscpu.per_cpu_threshold = 0.0
		} else {
			logger.Debug("'%s' = %f", perCpuThresholdKey, psutilscpu.per_cpu_threshold)
		}
	}

	if (psutilscpu.per_cpu_threshold == 0.0) && (psutilscpu.total_threshold == 0.0) {
		logger.Debug("'%s' and '%s' = 0.0. This is not allowed, plugin disabled", totalThresholdKey, perCpuThresholdKey)
		psutilscpu.enabled = false
	}

	return true
}

func (psutilsCpu *PsutilsCpu) logConfig() {
	logger := logging.GetLogger("")

	if logger != nil {
		logger.Info("psutil.cpu config: enabled=%t, per_cpu_threshold=%f, total_cpu_threshold=%f", psutilsCpu.enabled, psutilsCpu.per_cpu_threshold, psutilsCpu.total_threshold)
	}
}
