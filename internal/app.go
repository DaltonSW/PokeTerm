package internal

import (
	"github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/lipgloss/v2"
	"go.dalton.dog/poketerm/internal/styles"
)

var TitleStyle = lipgloss.NewStyle().Bold(true).Foreground(lipgloss.Color("#BADA55")).AlignHorizontal(lipgloss.Center)

const BaseURL = "https://pokeapi.co/api/v2"
const EndpointURL = BaseURL + "/%s"
const IdentifierURL = EndpointURL + "/%s"

type MainModel struct {
	cache *Cache
	list  ListModel

	ready         bool
	refGroupsLeft int
	initRefGroups []tea.Cmd

	viewportWrapper lipgloss.Style
}

func NewMainModel() (m MainModel) {
	m = MainModel{
		cache: NewCache(),
		list:  NewListModel(),
	}

	m.list.cache = m.cache

	refCmds := []tea.Cmd{
		LoadRefsCmd(Pokemon),
		LoadRefsCmd(Type),
		LoadRefsCmd(Ability),
		LoadRefsCmd(Move),
	}

	m.refGroupsLeft = len(refCmds)
	m.initRefGroups = refCmds

	m.viewportWrapper = lipgloss.NewStyle().BorderForeground(styles.BorderColor).Border(lipgloss.RoundedBorder()).Align(lipgloss.Center, lipgloss.Center)

	return m
}

func (m MainModel) Init() tea.Cmd {
	return tea.Batch(m.initRefGroups...)
}

func (m MainModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmds []tea.Cmd
	var cmd tea.Cmd

	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		if msg.String() == "ctrl+c" || msg.String() == "q" {
			return m, tea.Quit
		}
	case tea.WindowSizeMsg:
		leftWidth := min(60, msg.Width/2)
		m.list = m.list.UpdateSize(leftWidth, msg.Height)

		m.viewportWrapper = m.viewportWrapper.Width(msg.Width - leftWidth).Height(msg.Height)

	case RefsLoadedMsg:
		m.refGroupsLeft--
		if m.refGroupsLeft <= 0 {
			m.ready = true

			cmds = append(cmds, m.list.Init())
		}

	}

	m.list, cmd = m.list.Update(msg)
	cmds = append(cmds, cmd)

	return m, tea.Batch(cmds...)
}

func (m MainModel) View() string {
	if !m.ready {
		return "Loading references..."
	}

	leftContent := m.list.View()
	rightContent := m.viewportWrapper.Render("Coming soon!")

	return lipgloss.JoinHorizontal(lipgloss.Center, leftContent, rightContent)
}
