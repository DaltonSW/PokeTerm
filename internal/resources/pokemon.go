package resources

import (
	"github.com/charmbracelet/lipgloss/v2"
	"go.dalton.dog/poketerm/internal"
	"go.dalton.dog/poketerm/internal/api"
	"go.dalton.dog/poketerm/internal/styles"
)

type Pokemon struct {
	ID   int
	Name string
	URL  string
	Kind internal.ResKind

	Response pokemonAPIResponse

	BaseExp int
	Height  int // Units are 0.1m -- Ex: Ditto returns '3' and has a height of 0.3m
	Weight  int // Units are 0.1kg -- Ex: Ditto returns '40' and has a weight of 4kg

	Types        []*Type
	Abilities    []*Ability
	LearnedMoves []*Move
	HeldItems    []*Item

	CryLatestURL string
	CryLegacyURL string

	Sprites map[string]string // Mapping the name to the URL
	// Stats     []*Stat
	LocEncURL string

	// Stats
	//	Base
	//	EVs

	// Past Types
	// Past Abilities

	// Location Area Encounters (URL: /api/v2/pokemon/#/encounters)
	//	Returns a list of (Location Area, Version Details) pairs
}

// Moves []struct {
//	Move *Move
//	VersionGroupDetails []struct {
//		Level Learned At
//		Version Group
//		Move Learn Method
//		Order (sorting?)
//	}
// }

func (p *Pokemon) GetName() string               { return p.Name }
func (p *Pokemon) GetURL() string                { return p.URL }
func (p *Pokemon) GetKind() internal.ResKind     { return p.Kind }
func (p *Pokemon) SetKind(kind internal.ResKind) { p.Kind = kind }
func (p *Pokemon) GetRelated() []internal.ResourceRef {
	var refs []internal.ResourceRef
	for _, t := range p.Types {
		refs = append(refs, internal.ResourceRef{Kind: t.Kind, Name: t.Name, URL: t.URL})
	}

	for _, a := range p.Abilities {
		refs = append(refs, internal.ResourceRef{Kind: a.Kind, Name: a.Name, URL: a.URL})
	}
	return refs
}

func (p *Pokemon) GetPreview(cache *internal.Cache, width, height int) string {
	// outByte, err := json.MarshalIndent(&p.Response, "", "  ")
	// if err != nil {
	// 	return err.Error()
	// }
	// outStr, strErr := glamour.Render("```json\n"+string(outByte)+"\n```", "dark")
	//
	// if strErr != nil {
	// 	return strErr.Error()
	// }

	style := styles.ViewportStyle.Width(width).MaxWidth(width).Height(height).MaxHeight(height).Align(lipgloss.Center)

	// Title - Name
	// Subt. - Description ("The Balloon Pokemon")

	headStr := p.Name + "\n" + "The <something> Pokemon\n"

	// Types
	// Type Table

	typeStr := ""

	// Stats / EVs
	// Abilities
	// Gender Ratio
	// Catch Rate
	// Egg Groups
	// Hatch Time
	// Height / Weight
	// EXP / Leveling Rate

	return style.Render(lipgloss.JoinVertical(lipgloss.Center, headStr, typeStr))
}

type pokemonAPIResponse struct {
	ID   int    `json:"id"`
	Name string `json:"name"`

	Abilities []struct {
		Ability  api.RespPointer `json:"ability"`
		IsHidden bool
		Slot     int
	} `json:"abilities"`

	BaseExperience int `json:"base_experience,omitempty"`

	Cries struct {
		Latest string `json:"latest,omitempty"`
		Legacy string `json:"legacy,omitempty"`
	} `json:"cries"`

	Forms []api.RespPointer `json:"forms,omitempty"`

	// GameIndices

	Height int `json:"height,omitempty"`

	// HeldItems

	IsDefault bool `json:"is_default,omitempty"`

	LocationAreaEncounters string `json:"location_area_encounters,omitempty"` // URL pointing to encounters

	// Moves []struct{Move: api.RespPointer, VersionGroupDetails: []struct of more stuff}

	Order int `json:"order"` // I think this is used for sorting?

	// PastAbilities

	// PastTypes

	Species api.RespPointer `json:"species"`

	Sprites struct {
		BackDefault      string `json:"back_default,omitempty"`
		BackFemale       string `json:"back_female,omitempty"`
		BackShiny        string `json:"back_shiny,omitempty"`
		BackShinyFemale  string `json:"back_shiny_female,omitempty"`
		FrontDefault     string `json:"front_default,omitempty"`
		FrontFemale      string `json:"front_female,omitempty"`
		FrontShiny       string `json:"front_shiny,omitempty"`
		FrontShinyFemale string `json:"front_shiny_female,omitempty"`

		Other struct {
			DreamWorld struct {
				FrontDefault string `json:"front_default,omitempty"`
				FrontFemale  string `json:"front_female,omitempty"`
			} `json:"dream_world"`

			Home struct {
				FrontDefault     string `json:"front_default,omitempty"`
				FrontFemale      string `json:"front_female,omitempty"`
				FrontShiny       string `json:"front_shiny,omitempty"`
				FrontShinyFemale string `json:"front_shiny_female,omitempty"`
			} `json:"home"`

			OfficialArtwork struct {
				FrontDefault string `json:"front_default,omitempty"`
				FrontShiny   string `json:"front_shiny,omitempty"`
			} `json:"official_artwork"`

			Showdown struct {
				BackDefault      string `json:"back_default,omitempty"`
				BackFemale       string `json:"back_female,omitempty"`
				BackShiny        string `json:"back_shiny,omitempty"`
				BackShinyFemale  string `json:"back_shiny_female,omitempty"`
				FrontDefault     string `json:"front_default,omitempty"`
				FrontFemale      string `json:"front_female,omitempty"`
				FrontShiny       string `json:"front_shiny,omitempty"`
				FrontShinyFemale string `json:"front_shiny_female,omitempty"`
			} `json:"showdown"`
		} `json:"other"`

		Versions struct {
		} `json:"versions"`
	} `json:"sprites"`

	Stats []struct {
		BaseStat int             `json:"base_stat,omitempty"`
		Effort   int             `json:"effort,omitempty"`
		Stat     api.RespPointer `json:"stat"`
	} `json:"stats,omitempty"`

	Types []struct {
		Slot int             `json:"slot,omitempty"`
		Type api.RespPointer `json:"type"`
	} `json:"types,omitempty"`

	Weight int `json:"weight,omitempty"`
}

func init() {
	internal.RegisterLoader(internal.Pokemon, func(url string) (internal.Resource, error) {
		data, err := api.QueryAndUnmarshal[pokemonAPIResponse](url)
		if err != nil {
			return nil, err
		}

		p := &Pokemon{
			Name:         data.Name,
			URL:          url,
			ID:           data.ID,
			Kind:         internal.Pokemon,
			BaseExp:      data.BaseExperience,
			Height:       data.Height,
			Weight:       data.Weight,
			CryLatestURL: data.Cries.Latest,
			CryLegacyURL: data.Cries.Legacy,
			LocEncURL:    data.LocationAreaEncounters,
			Sprites:      make(map[string]string),
			Response:     data,
		}

		for _, a := range data.Abilities {
			p.Abilities = append(p.Abilities, &Ability{
				Name: a.Ability.Name,
				URL:  a.Ability.URL,
				Kind: internal.Ability,
			})
		}

		for _, t := range data.Types {
			p.Types = append(p.Types, &Type{
				Name: t.Type.Name,
				URL:  t.Type.URL,
				Kind: internal.Type,
			})
		}

		return p, nil
	})
}
