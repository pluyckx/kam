package logging

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"os"
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

type Logger struct {
	out    io.Writer
	level  level
	logger *log.Logger
	buffer bytes.Buffer
}

type FileLogger struct {
	Logger

	path string
	file *os.File
}

type LogEntry interface {
	GetModuleName() string
	GetMessage() string
}

type DefaultLogEntry struct {
	LogEntry

	ModuleName string
	Format     string
	Data       []interface{}

	buffer bytes.Buffer
}

func NewLogger(output io.Writer) *Logger {
	logger := Logger{out: output, level: defaultLevel}

	logger.logger = log.New(logger.out, "", log.Ldate|log.Ltime|log.Lshortfile)

	return &logger
}

func NewFileLogger(path string) (*FileLogger, error) {
	f, err := os.OpenFile(path, os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0664)

	if err != nil {
		return nil, err
	}

	logger := log.New(f, "", log.Ldate|log.Ltime|log.Lshortfile)

	return &FileLogger{Logger: Logger{out: f, level: defaultLevel, logger: logger}, path: path, file: f}, nil
}

func (logger *Logger) Error(entry LogEntry) {
	logger.buffer.Reset()

	fmt.Fprintf(&logger.buffer, "[%s - ERROR] ", entry.GetModuleName())
	fmt.Fprint(&logger.buffer, entry.GetMessage())

	if logger.level >= Level_Error {
		logger.logger.Print(logger.buffer.String())
		fmt.Println(logger.buffer.String())
	}

	panic(logger.buffer.String())
}

func (logger *Logger) Warning(entry LogEntry) {
	if logger.level >= Level_Warning {
		logger.buffer.Reset()

		fmt.Fprintf(&logger.buffer, "[%s - WARNING] ", entry.GetModuleName())
		fmt.Fprint(&logger.buffer, entry.GetMessage())

		logger.logger.Print(logger.buffer.String())
		fmt.Println(logger.buffer.String())
	}
}

func (logger *Logger) Info(entry LogEntry) {
	if logger.level >= Level_Info {
		logger.buffer.Reset()

		fmt.Fprintf(&logger.buffer, "[%s - INFO] ", entry.GetModuleName())
		fmt.Fprint(&logger.buffer, entry.GetMessage())

		logger.logger.Print(logger.buffer.String())
		fmt.Println(logger.buffer.String())
	}
}

func (logger *Logger) Debug(entry LogEntry) {
	if logger.level >= Level_Debug {
		logger.buffer.Reset()

		fmt.Fprintf(&logger.buffer, "[%s - DEBUG] ", entry.GetModuleName())
		fmt.Fprint(&logger.buffer, entry.GetMessage())

		logger.logger.Print(logger.buffer.String())
		fmt.Println(logger.buffer.String())
	}
}

func (logger *Logger) SetLevel(level level) {
	logger.level = level
}

func (logger *FileLogger) Close() error {
	return logger.file.Close()
}

func (entry *DefaultLogEntry) GetModuleName() string {
	return entry.ModuleName
}

func (entry *DefaultLogEntry) GetMessage() string {
	if entry.buffer.Len() == 0 {
		fmt.Fprintf(&entry.buffer, entry.Format, entry.Data...)
	}

	return entry.buffer.String()
}
