package internal

import (
	"sort"

	"github.com/charmbracelet/bubbles/v2/list"
	"github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/lipgloss/v2"
)

var TitleStyle = lipgloss.NewStyle().Bold(true).Foreground(lipgloss.Color("#BADA55")).AlignHorizontal(lipgloss.Center)

const BaseURL = "https://pokeapi.co/api/v2"
const EndpointURL = BaseURL + "/%s"
const IdentifierURL = EndpointURL + "/%s"

type MainModel struct {
	cache *Cache
	list  list.Model

	ready         bool
	refGroupsLeft int
	initRefGroups []tea.Cmd
}

func NewMainModel() (m MainModel) {
	m = MainModel{
		cache: NewCache(),
	}

	refCmds := []tea.Cmd{
		LoadRefsCmd(Pokemon),
		LoadRefsCmd(Type),
		LoadRefsCmd(Ability),
		LoadRefsCmd(Move),
	}

	m.refGroupsLeft = len(refCmds)
	m.initRefGroups = refCmds

	del := NewDelegate()
	l := list.New(nil, del, 0, 0)
	l.Title = "PokeTerm -- Resource Search"
	l.Styles.Title = del.styles.Title
	l.SetShowHelp(true)
	l.SetShowFilter(true)
	l.SetFilteringEnabled(true)

	m.list = l

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
		m.list.SetWidth(msg.Width - 2)
		m.list.SetHeight(msg.Height - 2)
	case RefsLoadedMsg:
		refs := m.list.Items()

		for _, r := range msg.Refs {
			m.cache.RegisterRef(r)
			refs = append(refs, r)
		}

		sort.Slice(refs, func(i, j int) bool {
			refI := refs[i].(ResourceRef)
			refJ := refs[j].(ResourceRef)
			return refI.Name < refJ.Name
		})

		cmd = m.list.SetItems(refs)
		cmds = append(cmds, cmd)

		m.refGroupsLeft--
		if m.refGroupsLeft <= 0 {
			m.ready = true

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

	return m.list.View()
}
