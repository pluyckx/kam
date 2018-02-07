package config

import (
	"github.com/BurntSushi/toml"
)

type TomlSection struct {
	key      string
	sections map[string]interface{}
}

func LoadFile(configFile string) (*TomlSection, error) {
	var cfg TomlSection

	cfg.key = "__FILE__"

	_, err := toml.DecodeFile(configFile, &cfg.sections)

	return &cfg, err
}

func LoadData(data string) (*TomlSection, error) {
	var cfg TomlSection

	cfg.key = "__DATA__"

	_, err := toml.Decode(data, &cfg.sections)

	return &cfg, err
}

func (section *TomlSection) GetSectionList() []string {
	sections := []string{}

	for k, v := range section.sections {

		_, ok := v.(map[string]interface{})

		if ok {
			sections = append(sections, k)
		}
	}

	return sections
}

func (section *TomlSection) Section(name string) *TomlSection {
	if child, ok := section.sections[name]; ok {
		if m, ok := child.(map[string]interface{}); ok {
			return &TomlSection{key: name, sections: m}
		} else {
			return nil
		}
	} else {
		return nil
	}
}

func (section *TomlSection) GetString(key string) (string, bool) {
	if child, ok := section.sections[key]; ok {
		value, ok := child.(string)

		return value, ok
	} else {
		return "", false
	}
}

func (section *TomlSection) GetInteger(key string) (int64, bool) {
	if child, ok := section.sections[key]; ok {
		value, ok := child.(int64)

		return value, ok
	} else {
		return 0, false
	}
}

func (section *TomlSection) GetStringArray(key string) ([]string, bool) {
	if child, ok := section.sections[key]; ok {
		interfaces, ok := child.([]interface{})

		if !ok {
			return []string{}, false
		}

		var strings []string

		for _, i := range interfaces {
			tmp, ok := i.(string)

			if !ok {
				return []string{}, false
			}

			strings = append(strings, tmp)
		}

		if !ok {
			return []string{}, false
		} else {
			return strings, true
		}
	} else {
		return []string{}, false
	}
}
