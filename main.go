package main

import (
	"go.dalton.dog/poketerm/cmd"
	_ "go.dalton.dog/poketerm/internal/resources" // Load to run resource init funcs
)

// Entry point of the program, starts up the BubbleTea program
func main() {
	cmd.Execute()
}
