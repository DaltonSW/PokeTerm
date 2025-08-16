package internal

import (
	"fmt"

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

	ready bool

	initRefGroups []tea.Cmd
	refGroupsLeft int

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
		switch msg.String() {
		case "ctrl+c":
			return m, tea.Quit
		case "enter":
			ref, ok := m.list.CurrentResource()
			if ok {
				if !m.cache.IsLoaded(ref) && !m.cache.IsLoading(ref) {
					m.cache.MarkLoading(ref)
					cmds = append(cmds, LoadCmd(ref))
				}

			}
		default:
			m.list, cmd = m.list.Update(msg)
			cmds = append(cmds, cmd)

		}

	case tea.WindowSizeMsg:
		leftWidth := min(60, msg.Width/2)
		m.list = m.list.UpdateSize(leftWidth, msg.Height)

		m.viewportWrapper = m.viewportWrapper.Width(msg.Width - leftWidth).Height(msg.Height)

	case RefsLoadedMsg:
		m.list, cmd = m.list.Update(msg)
		cmds = append(cmds, cmd)
		m.refGroupsLeft--
		if m.refGroupsLeft <= 0 {
			m.ready = true

			cmds = append(cmds, m.list.Init())
		}

	case ResourceLoadedMsg:
		m.cache.Store(msg.Kind, msg.Resource)

	default:
		m.list, cmd = m.list.Update(msg)
		cmds = append(cmds, cmd)
	}

	return m, tea.Batch(cmds...)
}

func (m MainModel) View() string {
	var left, right string

	if !m.ready {
		right = "Loading references..."
	}

	left = m.list.View()

	item, ok := m.list.CurrentResource()
	if ok {
		res, loaded := m.cache.Get(item)
		if loaded && res != nil {
			right = res.GetPreview()
		} else {
			right = fmt.Sprintf("Loading resource: %v from %v", item.Name, item.URL)
		}

	} else {
		right = "Currently selected thing didn't return a proper ResourceRef"
	}
	right = m.viewportWrapper.Render(right)

	return lipgloss.JoinHorizontal(lipgloss.Center, left, right)
}
