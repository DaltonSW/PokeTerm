package models

import (
	"fmt"

	"github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/lipgloss/v2"
)

var TitleStyle = lipgloss.NewStyle().Bold(true).Foreground(lipgloss.Color("#BADA55")).AlignHorizontal(lipgloss.Center)

const BaseURL = "https://pokeapi.co/api/v2/%s?limit=2000"

type MainModel struct {
	loaders []ResourceLoaderModel

	err error
}

func NewModel() (m MainModel) {
	m.loaders = make([]ResourceLoaderModel, 0)

	m.loaders = append(m.loaders, NewResourceLoader("pokemon", BaseURL))
	m.loaders = append(m.loaders, NewResourceLoader("type", BaseURL))
	m.loaders = append(m.loaders, NewResourceLoader("ability", BaseURL))
	m.loaders = append(m.loaders, NewResourceLoader("machine", BaseURL))

	return
}

func (m MainModel) Init() tea.Cmd {
	var cmds []tea.Cmd
	var cmd tea.Cmd
	for _, loader := range m.loaders {
		cmd = loader.Init()
		cmds = append(cmds, cmd)
	}
	return tea.Batch(cmds...)
}

func (m MainModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmds []tea.Cmd

	for i, loader := range m.loaders {
		outLoad, cmd := loader.Update(msg)
		cmds = append(cmds, cmd)
		m.loaders[i] = outLoad
	}

	return m, tea.Batch(cmds...)
}

func (m MainModel) View() string {
	if m.err != nil {
		return fmt.Sprintf("Error occurred: %v", m.err)
	}

	var s string

	s = TitleStyle.Render("Loading stuff\n")

	for _, loader := range m.loaders {
		s += fmt.Sprintf("\n%s\n", loader.View())
	}

	return s
}
