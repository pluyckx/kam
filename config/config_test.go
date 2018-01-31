package config

import (
	"os"
	"testing"
)

var configData string = `
[Default]
param1 = "this is some text"
param2 = -12345
param3 = 9876543210

[section2]
bool1 = false
bool2 = true

[section2.subsection]
number_array = [1, 2, 3, 4, 5]
string_array = [ "this", "is", "some", "text"]
`

var msg = "%v: expected %v, received %v\n"

var cfg *TomlSection

func TestMain(m *testing.M) {
	var err error
	cfg, err = LoadData(configData)

	if err != nil {
		panic(err)
	}

	os.Exit(m.Run())
}

func TestVerifySectionListRoot(t *testing.T) {
	sections := cfg.GetSectionList()

	if len(sections) != 2 {
		t.Errorf(msg, "len(sections)", 2, len(sections))
	} else {
		if sections[0] != "Default" {
			t.Errorf(msg, "sections[0]", "Default", sections[0])

			if sections[1] != "section2" {
				t.Errorf(msg, "sections[1]", "section2", sections[1])
			}
		}
	}

	if t.Failed() {
		t.Errorf("Found sections: %v\n", sections)
	}
}

func TestVerifySubSectionList(t *testing.T) {
	section := cfg.Section("section2")

	sections := section.GetSectionList()

	if len(sections) != 1 {
		t.Errorf(msg, "len(sections)", 1, len(sections))
	} else {
		if sections[0] != "subsection" {
			t.Errorf(msg, "sections[0]", "subsection", sections[0])
		}
	}

	if t.Failed() {
		t.Errorf("Found sections: %v\n", sections)
	}
}

func TestGetSection_Existing(t *testing.T) {
	section := cfg.Section("Default")

	if section == nil {
		t.Errorf(msg, "Section", "Default", nil)
	}
}

func TestGetSection_SubSection(t *testing.T) {
	section := cfg.Section("section2")

	if section != nil {
		subsection := section.Section("subsection")

		if subsection == nil {
			t.Errorf(msg, "Subsection", "subsection", nil)
		}
	} else {
		if section != nil {
			t.Errorf(msg, "Section", "section2", nil)
		}
	}
}

func TestGetSection_SubSection_NonExisting(t *testing.T) {
	section := cfg.Section("section2")

	if section != nil {
		subsection := section.Section("subsection_nonexisting")

		if subsection != nil {
			t.Errorf(msg, "Subsection", "nil", subsection.key)
		}
	} else {
		if section != nil {
			t.Errorf(msg, "Section", "section2", nil)
		}
	}
}

func TestGetSection_NonExisting(t *testing.T) {
	section := cfg.Section("Default_nonexisting")

	if section != nil {
		t.Errorf(msg, "Section", "nil", section.key)
	}
}

func TestGetSection_Case(t *testing.T) {
	section := cfg.Section("default")

	if section != nil {
		t.Errorf(msg, "Section", nil, section.key)
	}
}

func TestGetSection_TryParam(t *testing.T) {
	section := cfg.Section("Default")

	if section == nil {
		t.Errorf(msg, "Section", "Default", section.key)
	} else {
		paramAsSection := section.Section("param1")

		if paramAsSection != nil {
			t.Errorf(msg, "Section", nil, paramAsSection.key)
		}
	}
}

func TestGetString_Valid(t *testing.T) {
	section := cfg.Section("Default")

	if section != nil {
		value, ok := section.GetString("param1")

		if !ok {
			t.Errorf(msg, "String", true, ok)
		} else if value != "this is some text" {
			t.Errorf(msg, "String", "this is some text", value)
		}
	} else {
		t.Errorf(msg, "Section", "Default", section.key)
	}
}

func TestGetString_Invalid(t *testing.T) {
	section := cfg.Section("Default")

	if section != nil {
		value, ok := section.GetString("param2")

		if ok {
			t.Errorf(msg, "String", false, ok)
			t.Errorf(msg, "String", "", value)
		}
	} else {
		t.Errorf(msg, "Section", "Default", section.key)
	}
}

func TestGetString_NonExisting(t *testing.T) {
	section := cfg.Section("Default")

	if section != nil {
		value, ok := section.GetString("param1_doesnotexist")

		if ok {
			t.Errorf(msg, "String", false, ok)
			t.Errorf(msg, "String", "", value)
		}
	} else {
		t.Errorf(msg, "Section", "Default", section.key)
	}
}

func TestGetInteger_Valid(t *testing.T) {
	section := cfg.Section("Default")

	if section != nil {
		value, ok := section.GetInteger("param2")

		if !ok {
			t.Errorf(msg, "Integer", true, ok)
		} else if value != -12345 {
			t.Errorf(msg, "Integer", -12345, value)
		}
	} else {
		t.Errorf(msg, "Section", "Default", section.key)
	}
}

func TestGetInteger_ValidLarge(t *testing.T) {
	section := cfg.Section("Default")

	if section != nil {
		value, ok := section.GetInteger("param3")

		if !ok {
			t.Errorf(msg, "Integer", true, ok)
		} else if value != 9876543210 {
			t.Errorf(msg, "Integer", 9876543210, value)
		}
	} else {
		t.Errorf(msg, "Section", "Default", section.key)
	}
}

func TestGetInteger_Invalid(t *testing.T) {
	section := cfg.Section("Default")

	if section != nil {
		value, ok := section.GetInteger("param1")

		if ok {
			t.Errorf(msg, "Integer", false, ok)
			t.Errorf(msg, "Integer", 0, value)
		}
	} else {
		t.Errorf(msg, "Section", "Default", section.key)
	}
}

func TestGetInteger_NonExisting(t *testing.T) {
	section := cfg.Section("Default")

	if section != nil {
		value, ok := section.GetInteger("param2_doesnotexist")

		if ok {
			t.Errorf(msg, "Integer", false, ok)
			t.Errorf(msg, "Integer", 0, value)
		}
	} else {
		t.Errorf(msg, "Section", "Default", section.key)
	}
}
