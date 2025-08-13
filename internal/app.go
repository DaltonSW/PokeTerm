package internal

import (
	"fmt"

	"github.com/charmbracelet/bubbles/v2/progress"
	"github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/lipgloss/v2"
)

var TitleStyle = lipgloss.NewStyle().Bold(true).Foreground(lipgloss.Color("#BADA55")).AlignHorizontal(lipgloss.Center)

const BaseURL = "https://pokeapi.co/api/v2"
const EndpointURL = BaseURL + "/%s"
const IdentifierURL = EndpointURL + "/%s"

type MainModel struct {
	progress  progress.Model
	total     int
	completed int
	err       error
	cache     *Cache
}

func NewModel() (m MainModel) {
	m = MainModel{
		progress: progress.New(progress.WithDefaultGradient()),
		cache:    NewCache(),
	}

	m.total = 1
	m.cache.MarkLoading("type", "fire")

	return m
}

func (m MainModel) Init() tea.Cmd {
	return LoadCmd("type", "https://pokeapi.co/api/v2/type/fire")
}

func (m MainModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmds []tea.Cmd
	var cmd tea.Cmd

	switch msg := msg.(type) {

	case ResourceLoadedMsg:
		m.cache.Store(msg.Kind, msg.Resource)
		m.completed++
		cmd = m.progress.SetPercent(float64(m.completed) / float64(m.total))
		cmds = append(cmds, cmd)

		for _, ref := range msg.Resource.GetRelated() {
			m.queueResource(ref.Kind, ref.Name, ref.URL, &cmds)
		}

	case ErrMsg:
		m.err = msg
		return m, nil

	case tea.KeyMsg:
		if msg.String() == "q" {
			return m, tea.Quit
		}
	}

	m.progress, cmd = m.progress.Update(msg)
	cmds = append(cmds, cmd)

	return m, tea.Batch(cmds...)
}

func (m MainModel) View() string {
	if m.err != nil {
		return fmt.Sprintf("Error: %v\n", m.err)
	}

	s := fmt.Sprintf("Progress: %d/%d\n", m.completed, m.total)
	s += m.progress.View() + "\n"

	if m.completed == m.total && m.total > 0 {
		s += "\nAll loaded!\n"
		for kind, cache := range m.cache.loaded {
			s += fmt.Sprintf("%s loaded: %d\n", kind, len(cache))
		}
		s += "Press q to quit.\n"
	}

	return s
}

func (m *MainModel) queueResource(kind, name, url string, cmds *[]tea.Cmd) {
	if m.cache.IsLoaded(kind, name) || m.cache.IsLoading(kind, name) {
		return
	}
	m.cache.MarkLoading(kind, name)
	if cmds != nil {
		*cmds = append(*cmds, LoadCmd(kind, url))
	}
	m.total++
}
