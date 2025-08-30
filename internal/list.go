package internal

import (
	"fmt"
	"io"
	"sort"

	"github.com/charmbracelet/bubbles/v2/help"
	"github.com/charmbracelet/bubbles/v2/key"
	"github.com/charmbracelet/bubbles/v2/list"
	"github.com/charmbracelet/bubbles/v2/textinput"
	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/lipgloss/v2"
	"github.com/charmbracelet/log"
	"go.dalton.dog/poketerm/internal/styles"
	"golang.org/x/text/cases"
	"golang.org/x/text/language"
)

// ListModel represents a list of resource references that can be loaded/previewed
type ListModel struct {
	cache *Cache
	list  list.Model

	input     textinput.Model
	inputHelp help.Model
	active    bool

	style lipgloss.Style
}

var noFilteringKeymap = []key.Binding{
	key.NewBinding(
		key.WithKeys("/"),
		key.WithHelp("/", "filter"),
	),
	key.NewBinding(
		key.WithKeys("esc"),
		key.WithHelp("esc", "clear filter"),
	),
}

var whileFilteringKeymap = []key.Binding{
	// Filtering.
	key.NewBinding(
		key.WithKeys("enter", "tab", "shift+tab", "ctrl+k", "up", "ctrl+j", "down"),
		key.WithHelp("enter", "apply filter"),
	),
	key.NewBinding(
		key.WithKeys("esc"),
		key.WithHelp("esc", "cancel"),
	),
}

// NewListModel creates the list model
func NewListModel() ListModel {
	m := ListModel{}

	del := NewDelegate()
	l := list.New(nil, del, 0, 0)
	l.Styles.Title = del.styles.Item
	l.SetShowHelp(true)
	l.SetShowFilter(false)
	l.SetShowStatusBar(false)
	l.SetShowTitle(false)
	l.SetShowHelp(false)
	l.SetFilteringEnabled(true)
	m.list = l

	m.input = textinput.New()
	m.input.Placeholder = "<filter>"
	m.inputHelp = help.New()

	m.style = lipgloss.NewStyle().BorderForeground(styles.BorderColor).Border(lipgloss.RoundedBorder())

	return m
}

func (m ListModel) UpdateSize(w, h int) ListModel {
	m.style = m.style.Width(w)

	w = w - m.style.GetHorizontalBorderSize()
	m.input.SetWidth(w - len(m.input.Prompt) - 2)
	m.list.SetWidth(w)
	m.list.SetHeight(h - m.style.GetVerticalBorderSize() - lipgloss.Height(m.style.Render(m.input.View())) - 1)

	return m
}

func (m ListModel) CurrentResource() (ResourceRef, bool) {
	item := m.list.SelectedItem()
	res, ok := item.(ResourceRef)
	log.Debugf("Getting current resource from list: %s (%v)", res.Name, ok)
	return res, ok
}

func (m ListModel) Init() tea.Cmd {
	return m.input.Focus()
}

func (m ListModel) Update(msg tea.Msg) (ListModel, tea.Cmd) {
	var cmds []tea.Cmd
	var cmd tea.Cmd

	switch msg := msg.(type) {
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
	}

	m.list, cmd = m.list.Update(msg)
	cmds = append(cmds, cmd)

	// m.input, cmd = m.input.Update(msg)
	// cmds = append(cmds, cmd)

	m.input.SetValue(m.list.FilterValue())

	return m, tea.Batch(cmds...)
}

func (m ListModel) View() string {
	var helpStr string
	if m.list.FilterState() == list.Filtering {
		helpStr = m.inputHelp.ShortHelpView(whileFilteringKeymap)
	} else {
		helpStr = m.inputHelp.ShortHelpView(noFilteringKeymap)
	}
	return m.style.AlignHorizontal(lipgloss.Center).Render(m.input.View()+"\n"+helpStr) + "\n" + m.style.Render(m.list.View())
}

type ItemDelegate struct {
	styles styles.ListStyles
	caser  cases.Caser
}

func NewDelegate() ItemDelegate {
	del := ItemDelegate{}

	del.styles = styles.GetListStyles()
	del.caser = cases.Title(language.Und)

	return del
}

func (d ItemDelegate) Height() int                             { return 1 }
func (d ItemDelegate) Spacing() int                            { return 0 }
func (d ItemDelegate) Update(_ tea.Msg, _ *list.Model) tea.Cmd { return nil }
func (d ItemDelegate) Render(w io.Writer, m list.Model, index int, listItem list.Item) {
	resource, ok := listItem.(ResourceRef)
	if !ok {
		return
	}

	var matchedRunes []int
	title := d.caser.String(resource.Title())

	emptyFilter := m.SettingFilter() && m.FilterValue() == ""
	isFiltered := m.SettingFilter() || m.IsFiltered()

	if isFiltered && index < len(m.VisibleItems()) {
		// Get indices of matched characters
		matchedRunes = m.MatchesForItem(index)
	}

	if emptyFilter {
		title = d.styles.Item.Render(title)
	} else if isFiltered {
		var unmatched lipgloss.Style
		if index == m.Index() {
			unmatched = d.styles.Curr
		} else {
			unmatched = d.styles.Item
		}
		// Highlight matches
		matched := unmatched.Underline(true)
		title = lipgloss.StyleRunes(title, matchedRunes, matched, unmatched)
	}

	var str string

	if index == m.Index() {
		str = d.styles.Curr.Render(fmt.Sprintf("%s | %s", lipgloss.NewStyle().Width(8).Align(lipgloss.Right).Render(string(resource.Kind)), title))
	} else {
		str = fmt.Sprintf("%s | %s", d.styles.Desc.Render(string(resource.Kind)), d.styles.Item.Render(title))
	}

	fmt.Fprint(w, str)
}
