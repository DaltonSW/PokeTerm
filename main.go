package main

import (
	"os"

	"github.com/charmbracelet/log"

	"go.dalton.dog/poketerm/cmd"
	_ "go.dalton.dog/poketerm/internal/resources" // Load to run resource init funcs
)

const LogFile = "poketerm.log"

// Entry point of the program, starts up the BubbleTea program
func main() {
	// Setup debug logging
	file, err := os.OpenFile(LogFile, os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatal(err)
	}
	log.SetLevel(log.DebugLevel)
	log.SetTimeFormat("03:04:05.000")
	log.SetOutput(file)
	defer file.Close()

	log.Debug("Logging successfully started")

	// Enter program exection
	cmd.Execute()
}
