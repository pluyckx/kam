package main

import (
	"bytes"
	"fmt"

	"github.com/pluyckx/kam/logging"
)

func main() {
	var tmp bytes.Buffer
	var entry logging.DefaultLogEntry

	tmp.Reset()
	logger := logging.NewLogger(&tmp)

	logger.SetLevel(logging.Level_None)

	entry = logging.DefaultLogEntry{ModuleName: "Main", Format: "%v"}
	entry.Data = append(entry.Data, "test")

	logger.Error(&entry)

	fmt.Println("tmp:")
	fmt.Println(tmp.String())
}
