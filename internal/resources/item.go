package resources

import (
	"encoding/json"

	"github.com/charmbracelet/lipgloss/v2"
	"go.dalton.dog/poketerm/internal"
)

type Item struct {
	ID   int
	Name string
	URL  string
	Kind internal.ResKind
}

func (i *Item) GetName() string               { return i.Name }
func (i *Item) GetURL() string                { return i.URL }
func (i *Item) GetKind() internal.ResKind     { return i.Kind }
func (i *Item) SetKind(kind internal.ResKind) { i.Kind = kind }
func (i *Item) GetRelated() []internal.ResourceRef {
	var refs []internal.ResourceRef
	return refs
}

func (i *Item) GetPreview(cache *internal.Cache, width, height int) string {
	mainView := lipgloss.NewStyle().
		Width(width).MaxHeight(height).Height(height).
		Border(lipgloss.RoundedBorder()).BorderForeground(GetTypeColor(i.Name)).
		Align(lipgloss.Left)

	var outStr string

	content, err := json.MarshalIndent(i, "", "  ")
	if err != nil {
		outStr = err.Error()
	} else {
		outStr = string(content)
	}

	return mainView.Render(outStr)
}
