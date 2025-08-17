package internal

import (
	"fmt"

	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/lipgloss/v2"
	"github.com/charmbracelet/log"
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

	leftWidth     int
	width, height int
}

func NewMainModel() (m MainModel) {
	log.Debug("Creating MainModel")
	m = MainModel{
		cache: NewCache(),
		list:  NewListModel(),
	}

	m.list.cache = m.cache

	refCmds := []tea.Cmd{
		// LoadRefsCmd(Pokemon),
		LoadRefsCmd(Type),
		// LoadRefsCmd(Ability),
		// LoadRefsCmd(Move),
	}

	m.refGroupsLeft = len(refCmds)
	m.initRefGroups = refCmds

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
		default:
			m.list, cmd = m.list.Update(msg)
			cmds = append(cmds, cmd)

		}

	case tea.WindowSizeMsg:
		m.leftWidth = min(50, msg.Width/2)
		m.list = m.list.UpdateSize(m.leftWidth, msg.Height)

		m.width = msg.Width
		m.height = msg.Height

	case RefsLoadedMsg:
		m.list, cmd = m.list.Update(msg)
		cmds = append(cmds, cmd)
		m.refGroupsLeft--
		if m.refGroupsLeft <= 0 {
			m.ready = true
			cmds = append(cmds, m.list.Init())
		}
		log.Debug("Refs loaded", "kind", msg.Kind)

	case ResourceLoadedMsg:
		log.Debug("Resource loaded", "kind", msg.Kind, "name", msg.Resource.GetName())
		m.cache.Store(msg.Kind, msg.Resource)
		for _, ref := range msg.Resource.GetRelated() {
			if !m.cache.IsLoaded(ref) && !m.cache.IsLoading(ref) {
				m.cache.MarkLoading(ref)
				cmds = append(cmds, LoadCmd(ref))
			}
		}

	default:
		m.list, cmd = m.list.Update(msg)
		cmds = append(cmds, cmd)
	}

	ref, ok := m.list.CurrentResource()
	if ok {
		if !m.cache.IsLoaded(ref) && !m.cache.IsLoading(ref) {
			m.cache.MarkLoading(ref)
			cmds = append(cmds, LoadCmd(ref))
		}

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
		res, loaded := m.cache.GetFromRef(item)
		if loaded && res != nil {
			right = res.GetPreview(m.cache, m.width-m.leftWidth, m.height)
		} else {
			right = fmt.Sprintf("Loading resource: %v from %v", item.Name, item.URL)
		}

	} else {
		right = "Currently selected thing didn't return a proper ResourceRef"
	}
	return lipgloss.JoinHorizontal(lipgloss.Center, left, right)
}
