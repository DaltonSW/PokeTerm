package resources

import (
	"fmt"
	"strconv"

	"github.com/charmbracelet/lipgloss/v2"
	"github.com/charmbracelet/lipgloss/v2/table"
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

	Accuracy int
	Priority int // -8 to +8
	PP       int
	Power    int

	Target string
	Type   *Type

	Generation  string
	DamageClass string

	Ailment  string
	Category string
	CritRate int
	Drain    int
	Healing  int

	MinHits, MinTurns int
	MaxHits, MaxTurns int

	AilmentChance int
	FlinchChance  int
	StatChance    int
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
		Foreground(m.Type.GetColor()).
		Bold(true).Italic(true).Underline(true).
		AlignHorizontal(lipgloss.Center).
		Render(utils.StripAndTitle(m.Name) + "\n")

	infoTable := m.getInfoTable()

	mainAreaHeight := height - lipgloss.Height(title) - lipgloss.Height(infoTable) - 1
	style := lipgloss.NewStyle().MaxWidth(width).Height(height).Align(lipgloss.Left, lipgloss.Top).Padding(1, 1, 0)

	if len(m.LearnedByPokemon) < 1 {
		return style.Render(lipgloss.JoinVertical(lipgloss.Center, title, infoTable))
	}

	mainView := lipgloss.NewStyle().
		Width(lipgloss.Width(infoTable)).MaxHeight(mainAreaHeight-style.GetVerticalPadding()).
		Align(lipgloss.Left, lipgloss.Top).Border(lipgloss.RoundedBorder()).BorderForeground(m.Type.GetColor())

	pokeList := internal.ResourceToList(m.LearnedByPokemon, mainAreaHeight-mainView.GetVerticalFrameSize()-1, cache, true)

	headerStyle := lipgloss.NewStyle().AlignHorizontal(lipgloss.Center).
		Width(lipgloss.Width(infoTable)).Bold(true)

	pokesHeader := headerStyle.Render(fmt.Sprintf("~ Pokemon (%v) ~", len(m.LearnedByPokemon)))

	pokesHalf := lipgloss.JoinVertical(lipgloss.Center, pokesHeader, mainView.Render(pokeList.String()))

	mainSplit := lipgloss.JoinVertical(lipgloss.Center, infoTable, pokesHalf)

	return style.Render(lipgloss.JoinVertical(lipgloss.Center, title, mainSplit))
}

func (m *Move) getInfoTable() string {
	rows := [][]string{
		// {"Power", strconv.Itoa(m.Power)},
		// {"PP", strconv.Itoa(m.PP)},
		// {"Priority", strconv.Itoa(m.Priority)},
		// {"Stat Chance", strconv.Itoa(m.StatChance)},
		// {"Target", m.Target},
		// {"Type", m.Type.Name},
	}

	// Accuracy
	var acc string
	if m.Accuracy == 0 {
		acc = "Always"
	} else {
		acc = strconv.Itoa(m.Accuracy)
	}
	rows = append(rows, []string{"Accuracy", acc})

	// Ailment
	if m.Ailment != "" {
		rows = append(rows, []string{"Ailment", m.Ailment})
		rows = append(rows, []string{"Ailment Chance", strconv.Itoa(m.AilmentChance)})
	}

	// Category
	if m.Category != "" {
		rows = append(rows, []string{"Category", utils.StripAndTitle(m.Category)})
	}

	// Crit Rate
	if m.CritRate != 0 {
		rows = append(rows, []string{"Crit Rate", strconv.Itoa(m.CritRate)})
	}

	// Damage Class
	if m.DamageClass != "" {
		rows = append(rows, []string{"Damage Class", m.DamageClass})
	}

	// FlinchChance
	if m.FlinchChance != 0 {
		rows = append(rows, []string{"Flinch Chance", strconv.Itoa(m.FlinchChance)})
	}

	// Generation
	if m.Generation != "" {
		rows = append(rows, []string{"Generation", utils.StripAndTitle(m.Generation)})
	}

	// Healing
	if m.Healing != 0 {
		rows = append(rows, []string{"Healing", strconv.Itoa(m.Healing)})
	}

	// # Hits
	var numHits string
	if m.MinHits == 0 {
		numHits = "1"
	} else {
		numHits = fmt.Sprintf("%d - %d", m.MinHits, m.MaxHits)
	}
	rows = append(rows, []string{"# Hits", numHits})

	// # Turns
	if m.MinTurns != 0 {
		rows = append(rows, []string{"# Turns", fmt.Sprintf("%d - %d", m.MinTurns, m.MaxTurns)})
	}

	// {"Power", strconv.Itoa(m.Power)},
	// {"PP", strconv.Itoa(m.PP)},
	// {"Priority", strconv.Itoa(m.Priority)},
	// {"Stat Chance", strconv.Itoa(m.StatChance)},
	// {"Target", m.Target},
	// {"Type", m.Type.Name},

	rows = append(rows, []string{"Power", strconv.Itoa(m.Power)})
	rows = append(rows, []string{"PP", strconv.Itoa(m.PP)})
	rows = append(rows, []string{"Priority", strconv.Itoa(m.Priority) + " (-8 to +8)"})

	// Stat Chance
	if m.StatChance != 0 {
		rows = append(rows, []string{"Stat Chance", strconv.Itoa(m.StatChance)})
	}

	rows = append(rows, []string{"Target", utils.StripAndTitle(m.Target)})
	rows = append(rows, []string{"Type", lipgloss.NewStyle().Foreground(GetTypeColor(m.Type.Name)).Render(utils.StripAndTitle(m.Type.Name))})

	table := table.New().BorderStyle(lipgloss.NewStyle().Foreground(m.Type.GetColor())).Rows(rows...)

	return table.String()
}

type moveAPIResponse struct {
	ID   int    `json:"id"`
	Name string `json:"name"`

	Pokemon []api.RespPointer `json:"learned_by_pokemon"`

	Accuracy int `json:"accuracy,omitempty"`
	Priority int `json:"priority,omitempty"`
	PP       int `json:"pp,omitempty"`
	Power    int `json:"power,omitempty"`

	Target api.RespPointer `json:"target"`
	Type   api.RespPointer `json:"type"`

	Generation  api.RespPointer `json:"generation"`
	DamageClass api.RespPointer `json:"damage_class"`

	Meta struct {
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
		m.Type = &Type{Name: data.Type.Name, URL: url, ID: data.ID, Kind: internal.Type}

		m.Generation = data.Generation.Name

		return m, nil
	})
}
