package resources

import (
	"fmt"

	"github.com/charmbracelet/lipgloss/v2"
	"go.dalton.dog/poketerm/internal"
	"go.dalton.dog/poketerm/internal/api"
	"go.dalton.dog/poketerm/internal/utils"
)

// - Name
// - Accuracy
// - Effect Chance
// - PP
// - Priority
// - Power
// - Learned By Pokemon (list of name/URLs)
// - Generation.Name (name/URL)
// - Damage Class (physical, special, status)
// - Type
// - Target

// - Meta.Ailment (Name is fine, nothing very relevant stored in move-ailment endpoint)
// - Meta.Category (Name is fine, nothing very relevant stored in move-category endpoint)
// - Meta.CritRate
// - Meta.Drain
// - Meta.FlinchChance
// - Meta.Healing
// - Meta.MaxHits
// - Meta.MinHits
// - Meta.MaxTurns
// - Meta.MinTurns
// - Meta.StatChance

type Move struct {
	ID   int
	Name string
	URL  string
	Kind internal.ResKind

	LearnedByPokemon []*Pokemon

	PP    int
	Power int
	Type  *Type

	Generation string
	Target     string

	Accuracy int
	Priority int // -8 to +8
}

func (m *Move) GetName() string               { return m.Name }
func (m *Move) GetURL() string                { return m.URL }
func (m *Move) GetKind() internal.ResKind     { return m.Kind }
func (m *Move) SetKind(kind internal.ResKind) { m.Kind = kind }
func (m *Move) GetRelated() []internal.ResourceRef {
	var refs []internal.ResourceRef
	for _, p := range m.LearnedByPokemon {
		refs = append(refs, internal.ResourceRef{Name: p.Name, Kind: p.Kind, URL: p.URL})
	}
	return refs
}

func (m *Move) GetPreview(cache *internal.Cache, width, height int) string {

	title := lipgloss.NewStyle().MaxWidth(width).
		Foreground(GetTypeColor(m.Name)).
		Bold(true).Italic(true).Underline(true).
		AlignHorizontal(lipgloss.Center).
		Render(utils.StripAndTitle(m.Name) + "\n")

	mainAreaHeight := height - lipgloss.Height(title) - 1

	mainView := lipgloss.NewStyle().
		MaxWidth(width).MaxHeight(mainAreaHeight).Height(mainAreaHeight).
		Border(lipgloss.RoundedBorder()).Align(lipgloss.Left)

	sPokes := internal.ResourceToList(m.LearnedByPokemon, mainAreaHeight-mainView.GetVerticalFrameSize(), cache, true)

	headerStyle := lipgloss.NewStyle().AlignHorizontal(lipgloss.Center).
		Width(mainView.GetWidth()).Bold(true)

	pokesHeader := headerStyle.Render(fmt.Sprintf("~ Pokemon (%v) ~", len(m.LearnedByPokemon)))

	pokesHalf := lipgloss.JoinVertical(lipgloss.Center, pokesHeader, mainView.Render(sPokes.String()))

	return lipgloss.JoinVertical(lipgloss.Center, title, pokesHalf)
}

type moveAPIResponse struct {
	ID   int    `json:"id"`
	Name string `json:"name"`

	Pokemon []api.RespPointer `json:"learned_by_pokemon"`

	Accuracy int `json:"accuracy,omitempty"`
	Priority int `json:"priority,omitempty"`
	PP       int `json:"pp,omitempty"`
	Power    int `json:"power,omitempty"`

	Target     api.RespPointer `json:"target"`
	Type       api.RespPointer `json:"type"`
	Generation api.RespPointer `json:"generation"`

	DamageClass api.RespPointer `json:"damage_class"`
	Meta        struct {
		Ailment       api.RespPointer `json:"ailment"`
		AilmentChance int             `json:"ailment_chance,omitempty"`
		Category      api.RespPointer `json:"category"`
		CritRate      int             `json:"crit_rate,omitempty"`
		Drain         int             `json:"drain,omitempty"`
		FlinchChance  int             `json:"flinch_chance,omitempty"`
		Healing       int             `json:"healing,omitempty"`
		MaxHits       int             `json:"max_hits,omitempty"`
		MinHits       int             `json:"min_hits,omitempty"`
		MaxTurns      int             `json:"max_turns,omitempty"`
		MinTurns      int             `json:"min_turns,omitempty"`
		StatChance    int             `json:"stat_chance,omitempty"`
	} `json:"meta"`
}

func init() {
	internal.RegisterLoader(internal.Move, func(url string) (internal.Resource, error) {
		data, err := api.QueryAndUnmarshal[moveAPIResponse](url)
		if err != nil {
			return nil, err
		}
		m := &Move{Name: data.Name, URL: url, ID: data.ID, Kind: internal.Move}
		for _, p := range data.Pokemon {
			m.LearnedByPokemon = append(m.LearnedByPokemon, &Pokemon{
				Name: p.Name,
				URL:  p.URL,
				Kind: internal.Pokemon,
			})
		}

		m.Accuracy = data.Accuracy
		m.Priority = data.Priority
		m.Power = data.Power
		m.PP = data.PP

		m.Target = data.Target.Name
		m.Generation = data.Generation.Name

		m.Type = &Type{Name: data.Type.Name, URL: url, ID: data.ID, Kind: internal.Type}

		return m, nil
	})
}
