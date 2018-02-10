package logging

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"os"
	"sync"
)

type level uint32

const (
	Level_None    level = iota
	Level_Error   level = iota
	Level_Warning level = iota
	Level_Info    level = iota
	Level_Debug   level = iota
)

const defaultLevel = Level_Warning

type Logger interface {
	Error(format string, params ...interface{})
	Warning(format string, params ...interface{})
	Info(format string, params ...interface{})
	Debug(format string, params ...interface{})
	Log(level string, format string, params ...interface{})
	SetLevel(level level)
	GetLevel() level
}

type NullLogger struct {
}

type BaseLogger struct {
	out    io.Writer
	level  level
	logger *log.Logger
	buffer bytes.Buffer
}

type FileLogger struct {
	BaseLogger

	path string
	file *os.File
}

var _ Logger = (*BaseLogger)(nil)
var _ Logger = (*FileLogger)(nil)
var nullLogger Logger = &NullLogger{}

const defaultLoggerKey = "__default__"

var loggers map[string]Logger = make(map[string]Logger)
var syncCall sync.Mutex

func GetLogger(key string) Logger {
	var logger Logger
	var ok bool

	if key == "" {
		key = defaultLoggerKey
	}

	syncCall.Lock()
	logger, ok = loggers[key]
	syncCall.Unlock()

	if !ok {
		return nullLogger
	} else {
		return logger
	}
}

func RegisterLogger(key string, logger Logger) bool {
	var ret bool

	if key == "" {
		key = defaultLoggerKey
	}

	syncCall.Lock()
	if _, ok := loggers[key]; !ok {
		loggers[key] = logger

		ret = true
	} else {
		ret = false
	}
	syncCall.Unlock()

	return ret
}

func NewLogger(output io.Writer) *BaseLogger {
	logger := BaseLogger{out: output, level: defaultLevel}

	logger.logger = log.New(logger.out, "", log.Ldate|log.Ltime|log.Lshortfile)

	return &logger
}

func NewFileLogger(path string) (*FileLogger, error) {
	f, err := os.OpenFile(path, os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0664)

	if err != nil {
		return nil, err
	}

	logger := log.New(f, "", log.Ldate|log.Ltime|log.Lshortfile)

	return &FileLogger{BaseLogger: BaseLogger{out: f, level: defaultLevel, logger: logger}, path: path, file: f}, nil
}

func IsNullLogger(logger Logger) bool {
	return logger == nullLogger
}

func (logger *BaseLogger) Error(format string, params ...interface{}) {
	if logger.level >= Level_Error {
		logger.Log("Error", format, params...)
	} else {
		logger.buffer.Reset()

		fmt.Fprint(&logger.buffer, "[ERROR] ")
		fmt.Fprintf(&logger.buffer, format, params...)
	}

	panic(logger.buffer.String())
}

func (logger *BaseLogger) Warning(format string, params ...interface{}) {
	if logger.level >= Level_Warning {
		logger.Log("WARNING", format, params...)
	}
}

func (logger *BaseLogger) Info(format string, params ...interface{}) {
	if logger.level >= Level_Info {
		logger.Log("INFO", format, params...)
	}
}

func (logger *BaseLogger) Debug(format string, params ...interface{}) {
	if logger.level >= Level_Debug {
		logger.Log("DEBUG", format, params...)
	}
}

func (logger *BaseLogger) Log(level string, format string, params ...interface{}) {
	logger.buffer.Reset()

	logger.buffer.WriteRune('[')
	logger.buffer.WriteString(level)
	logger.buffer.WriteString("] ")

	fmt.Fprintf(&logger.buffer, format, params...)

	logger.logger.Output(3, logger.buffer.String())
	fmt.Println(logger.buffer.String())
}

func (logger *BaseLogger) SetLevel(level level) {
	logger.level = level
}

func (logger *BaseLogger) GetLevel() level {
	return logger.level
}

func (logger *FileLogger) Log(level string, format string, params ...interface{}) {
	logger.BaseLogger.Log(level, format, params...)
	logger.Sync()
}

func (logger *FileLogger) Sync() error {
	return logger.file.Sync()
}

func (logger *FileLogger) Close() error {
	return logger.file.Close()
}

func (logger *NullLogger) Error(format string, params ...interface{}) {
}

func (logger *NullLogger) Warning(format string, params ...interface{}) {
}

func (logger *NullLogger) Info(format string, params ...interface{}) {
}

func (logger *NullLogger) Debug(format string, params ...interface{}) {
}

func (logger *NullLogger) Log(level string, format string, params ...interface{}) {

}

func (logger *NullLogger) SetLevel(level level) {
}

func (logger *NullLogger) GetLevel() level {
	return Level_None
}
