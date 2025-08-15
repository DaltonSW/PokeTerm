package internal

import (
	"fmt"
	"io"
	"strings"

	"github.com/charmbracelet/bubbles/v2/list"
	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/lipgloss/v2"
	"go.dalton.dog/poketerm/internal/styles"
	"golang.org/x/text/cases"
	"golang.org/x/text/language"
)

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

	color := resource.Kind.Color()
	resName := lipgloss.NewStyle().Foreground(color).Render(fmt.Sprintf("[%s] %s", resource.Kind.Icon(), d.caser.String(resource.Name)))

	str := fmt.Sprintf("%s %s", resName, d.styles.Desc.Render(resource.URL))

	fn := lipgloss.NewStyle().Render
	if index == m.Index() {
		fn = func(s ...string) string {
			return d.styles.Curr.Render("> " + strings.Join(s, " "))
		}
	} else {
		str = "  " + str
	}

	fmt.Fprint(w, fn(str))
}
