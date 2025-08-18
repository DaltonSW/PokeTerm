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
	// Set up debug logging
	file, err := os.Create(LogFile)
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
