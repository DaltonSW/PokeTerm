package cmd

import (
	"context"

	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/fang"
	"github.com/charmbracelet/log"
	"github.com/spf13/cobra"

	"go.dalton.dog/poketerm/internal"
)

const Version = "2.0.0-b1"

var rootCmd = &cobra.Command{
	Use:   "poketerm",
	Short: "Terminal-based PokeDex",
	Long:  "",
	Args:  cobra.ExactArgs(0),
	Run: func(cmd *cobra.Command, args []string) {
		model := internal.NewMainModel()
		program := tea.NewProgram(model, tea.WithAltScreen())

		if _, err := program.Run(); err != nil {
			log.Fatal(err)
		}
	},
}

func Execute() {
	if err := fang.Execute(context.Background(), rootCmd, fang.WithoutManpage(), fang.WithoutCompletions(), fang.WithVersion(Version)); err != nil {
		log.Fatal(err)
	}
}
