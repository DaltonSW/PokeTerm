package resources

import (
	"fmt"

	"github.com/charmbracelet/lipgloss/v2"
	"github.com/charmbracelet/lipgloss/v2/table"
	"go.dalton.dog/poketerm/internal"
	"go.dalton.dog/poketerm/internal/api"
	"go.dalton.dog/poketerm/internal/styles"
	"go.dalton.dog/poketerm/internal/utils"
)

type Ability struct {
	ID   int
	Name string
	URL  string
	Kind internal.ResKind

	Generation   string
	IsMainSeries bool

	EffectLong  string
	EffectShort string

	Pokemon []*Pokemon
}

func (a *Ability) GetName() string               { return a.Name }
func (a *Ability) GetURL() string                { return a.URL }
func (a *Ability) GetKind() internal.ResKind     { return a.Kind }
func (a *Ability) SetKind(kind internal.ResKind) { a.Kind = kind }
func (a *Ability) GetRelated() []internal.ResourceRef {
	var refs []internal.ResourceRef
	for _, p := range a.Pokemon {
		refs = append(refs, internal.ResourceRef{Name: p.Name, Kind: p.Kind, URL: p.URL})
	}
	return refs
}

func (a *Ability) GetPreview(cache *internal.Cache, width, height int) string {
	style := lipgloss.NewStyle().MaxWidth(width).Height(height).Align(lipgloss.Left, lipgloss.Top).Padding(1, 1, 0)

	title := lipgloss.NewStyle().MaxWidth(width).
		Foreground(styles.ForeColor).
		Bold(true).Italic(true).Underline(true).
		AlignHorizontal(lipgloss.Center).
		Render(utils.StripAndTitle(a.Name) + "\n")

	infoTable := a.getInfoTable(width - style.GetHorizontalFrameSize())

	mainAreaHeight := height - lipgloss.Height(title) - lipgloss.Height(infoTable) - 1

	if len(a.Pokemon) < 1 {
		return style.Render(lipgloss.JoinVertical(lipgloss.Center, title, infoTable))
	}

	mainView := lipgloss.NewStyle().
		Width(lipgloss.Width(infoTable)).MaxHeight(mainAreaHeight-style.GetVerticalPadding()).
		Align(lipgloss.Left, lipgloss.Top).Border(lipgloss.RoundedBorder()).BorderForeground(styles.ForeColor)

	pokeList := internal.ResourceToList(a.Pokemon, mainAreaHeight-mainView.GetVerticalFrameSize()-1, cache, true)

	headerStyle := lipgloss.NewStyle().AlignHorizontal(lipgloss.Center).
		Width(lipgloss.Width(infoTable)).Bold(true)

	pokesHeader := headerStyle.Render(fmt.Sprintf("~ Pokemon (%v) ~", len(a.Pokemon)))

	pokesHalf := lipgloss.JoinVertical(lipgloss.Center, pokesHeader, mainView.Render(pokeList.String()))

	mainSplit := lipgloss.JoinVertical(lipgloss.Center, infoTable, pokesHalf)

	return style.Render(lipgloss.JoinVertical(lipgloss.Center, title, mainSplit))
}

func (a *Ability) getInfoTable(width int) string {
	rows := [][]string{
		// {"Power", strconv.Itoa(m.Power)},
		// {"PP", strconv.Itoa(m.PP)},
		// {"Priority", strconv.Itoa(m.Priority)},
		// {"Stat Chance", strconv.Itoa(m.StatChance)},
		// {"Target", m.Target},
		// {"Type", m.Type.Name},
	}

	// Generation
	if a.Generation != "" {
		rows = append(rows, []string{"Generation", utils.StripAndTitle(a.Generation)})
	}

	// Effect
	if a.EffectLong != "" {
		rows = append(rows, []string{"Effect", a.EffectLong})
	}

	// Short Effect
	if a.EffectShort != "" {
		rows = append(rows, []string{"Short Effect", a.EffectShort})
	}

	table := table.New().Width(width).BorderStyle(lipgloss.NewStyle().Foreground(styles.ForeColor)).Rows(rows...).Wrap(true)

	return table.String()
}

type abilityAPIResponse struct {
	ID      int    `json:"id,omitempty"`
	Name    string `json:"name,omitempty"`
	Pokemon []struct {
		Pokemon api.RespPointer `json:"pokemon"`
	} `json:"pokemon,omitempty"`
	IsMainSeries  bool            `json:"is_main_series,omitempty"`
	Generation    api.RespPointer `json:"generation"`
	EffectEntries []struct {
		Effect      string          `json:"effect,omitempty"`
		Language    api.RespPointer `json:"language"`
		ShortEffect string          `json:"short_effect,omitempty"`
	} `json:"effect_entries,omitempty"`
}

func init() {
	internal.RegisterLoader(internal.Ability, func(url string) (internal.Resource, error) {
		data, err := api.QueryAndUnmarshal[abilityAPIResponse](url)
		if err != nil {
			return nil, err
		}
		a := &Ability{
			Name:         data.Name,
			URL:          url,
			ID:           data.ID,
			Kind:         internal.Ability,
			Generation:   data.Generation.Name,
			IsMainSeries: data.IsMainSeries,
		}
		for _, p := range data.Pokemon {
			a.Pokemon = append(a.Pokemon, &Pokemon{
				Name: p.Pokemon.Name,
				URL:  p.Pokemon.URL,
				Kind: internal.Pokemon,
			})
		}

		for _, effect := range data.EffectEntries {
			if effect.Language.Name == "en" {
				a.EffectLong = effect.Effect
				a.EffectShort = effect.ShortEffect
				break
			}
		}
		return a, nil
	})
}
