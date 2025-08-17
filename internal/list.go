package internal

import (
	"fmt"
	"io"
	"sort"

	"github.com/charmbracelet/bubbles/v2/list"
	"github.com/charmbracelet/bubbles/v2/textinput"
	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/lipgloss/v2"
	"go.dalton.dog/poketerm/internal/styles"
	"golang.org/x/text/cases"
	"golang.org/x/text/language"
)

type ListModel struct {
	cache *Cache
	list  list.Model

	input  textinput.Model
	active bool

	style lipgloss.Style
}

func NewListModel() ListModel {
	m := ListModel{}

	del := NewDelegate()
	l := list.New(nil, del, 0, 0)
	l.Styles.Title = del.styles.Item
	l.SetShowHelp(true)
	l.SetShowFilter(false)
	l.SetShowStatusBar(false)
	l.SetShowTitle(false)
	l.SetFilteringEnabled(true)
	m.list = l

	m.input = textinput.New()
	m.input.Placeholder = "/ to focus"

	m.style = lipgloss.NewStyle().BorderForeground(styles.BorderColor).Border(lipgloss.RoundedBorder())

	return m
}

func (m ListModel) UpdateSize(w, h int) ListModel {
	m.style = m.style.Width(w)

	w = w - m.style.GetHorizontalBorderSize()
	m.input.SetWidth(w - len(m.input.Prompt) - 2)
	m.list.SetWidth(w)
	m.list.SetHeight(h - m.style.GetVerticalBorderSize() - lipgloss.Height(m.style.Render(m.input.View())))

	return m
}

func (m ListModel) CurrentResource() (ResourceRef, bool) {
	item := m.list.SelectedItem()
	res, ok := item.(ResourceRef)
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

	m.input, cmd = m.input.Update(msg)
	cmds = append(cmds, cmd)

	m.input.SetValue(m.list.FilterValue())

	return m, tea.Batch(cmds...)
}

func (m ListModel) View() string {
	return m.style.Render(m.input.View()) + "\n" + m.style.Render(m.list.View())
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
func (d ItemDelegate) Spacing() int                            { return 1 }
func (d ItemDelegate) Update(_ tea.Msg, _ *list.Model) tea.Cmd { return nil }
func (d ItemDelegate) Render(w io.Writer, m list.Model, index int, listItem list.Item) {
	resource, ok := listItem.(ResourceRef)
	if !ok {
		return
	}

	// TODO: Make matching/highlighting less... bad. This is Frankenstein'd from list.DefaultDelegate

	// var matchedRunes []int
	// title := d.caser.String(resource.Title())
	//
	// isSelected := index == m.Index()
	// emptyFilter := m.SettingFilter() && m.FilterValue() == ""
	// isFiltered := m.SettingFilter() || m.IsFiltered()
	//
	// if isFiltered && index < len(m.VisibleItems()) {
	// 	// Get indices of matched characters
	// 	matchedRunes = m.MatchesForItem(index)
	// }
	//
	// if emptyFilter {
	// 	title = d.styles.Desc.Render(title)
	// } else if isSelected && !m.SettingFilter() {
	// 	if isFiltered {
	// 		// Highlight matches
	// 		unmatched := d.styles.Desc.Inline(true).Italic(false)
	// 		matched := unmatched.Foreground(styles.ForeColor).Underline(true)
	// 		title = lipgloss.StyleRunes(title, matchedRunes, matched, unmatched)
	// 	}
	// 	title = d.styles.Title.Foreground(resource.Kind.Color()).Render(title)
	// } else {
	// 	if isFiltered {
	// 		// Highlight matches
	// 		unmatched := d.styles.Desc.Inline(true).Italic(false)
	// 		matched := unmatched.Foreground(styles.ForeColor).Underline(true)
	// 		title = lipgloss.StyleRunes(title, matchedRunes, matched, unmatched)
	// 	}
	// 	title = d.styles.Title.Foreground(resource.Kind.Color()).Render(title)
	// }

	var str string

	if index == m.Index() {
		str = d.styles.Curr.Render(fmt.Sprintf("%s | %s", lipgloss.NewStyle().Width(8).Align(lipgloss.Right).Render(string(resource.Kind)), resource.Title()))
	} else {
		str = fmt.Sprintf("%s | %s", d.styles.Desc.Render(string(resource.Kind)), d.styles.Item.Render(resource.Title()))
	}

	fmt.Fprint(w, str)
}
