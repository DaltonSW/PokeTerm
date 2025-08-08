package cmd

import (
	"context"
	"fmt"
	"os"

	_ "github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/fang"
	"github.com/charmbracelet/log"
	"github.com/spf13/cobra"
)

const Version = "0.0.1"

var rootCmd = &cobra.Command{
	Use:   "poketerm",
	Short: "",
	Long:  "",
	Args:  cobra.ExactArgs(0),
	Run: func(cmd *cobra.Command, args []string) {
		log.Info("Coming soon!")
		// model := models.NewModel(args[0])
		//
		// p := tea.NewProgram(
		// 	model,
		// 	tea.WithAltScreen(),       // Use the full size of the terminal
		// 	tea.WithMouseCellMotion(), // Enable tracking the mouse wheel
		// )
		//
		// if _, err := p.Run(); err != nil {
		// 	log.Fatalf("Error running program:\n%v", err)
		// }
	},
}

func Execute() {
	if err := fang.Execute(context.Background(), rootCmd, fang.WithoutManpage(), fang.WithoutCompletions(), fang.WithVersion(Version)); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
