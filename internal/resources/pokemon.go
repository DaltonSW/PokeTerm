package resources

import (
	"strings"

	"github.com/charmbracelet/lipgloss/v2"
	"github.com/charmbracelet/lipgloss/v2/table"
	"go.dalton.dog/poketerm/internal"
	"go.dalton.dog/poketerm/internal/api"
	"go.dalton.dog/poketerm/internal/styles"
	"go.dalton.dog/poketerm/internal/utils"
)

type Pokemon struct {
	ID   int
	Name string
	URL  string
	Kind internal.ResKind

	Response pokemonAPIResponse

	BaseExp       int
	BaseHappiness int
	CaptureRate   int
	Color         string
	GenderRatio   int
	GrowthRate    string
	Habitat       string
	HatchCounter  int
	IsBaby        bool
	IsLegendary   bool
	IsMythical    bool
	Shape         string

	Height int // Units are 0.1m -- Ex: Ditto returns '3' and has a height of 0.3m
	Weight int // Units are 0.1kg -- Ex: Ditto returns '40' and has a weight of 4kg

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
	// outByte, err := json.MarshalIndent(&p, "", "  ")
	// if err != nil {
	// 	return err.Error()
	// }
	// outStr, strErr := glamour.Render("```json\n"+string(outByte)+"\n```", "dark")
	//
	// if strErr != nil {
	// 	return strErr.Error()
	// }

	// Title - Name
	// Subt. - Description ("The Balloon Pokemon") (This is actually apparently the 'Genera')

	headStr := utils.StripAndTitle(p.Name) + "\n" + "The <something> Pokemon\n"

	// Types
	// Type Table

	typeStr := p.getTypeInfo(cache)

	// Stats / EVs
	// Abilities
	// Gender Ratio
	// Catch Rate
	// Egg Groups
	// Hatch Time
	// Height / Weight
	// EXP / Leveling Rate

	style := styles.ViewportStyle.MaxWidth(width).Height(height).MaxHeight(height).Align(lipgloss.Center)

	return style.Render(lipgloss.JoinVertical(lipgloss.Center, headStr, typeStr))
}

func (p *Pokemon) getTypeInfo(cache *internal.Cache) string {
	if len(p.Types) == 0 {
		return "Typeless"
	}

	typeStr := p.Types[0].GetName()

	outStr := lipgloss.NewStyle().Foreground(GetTypeColor(typeStr)).Render(utils.StripAndTitle((typeStr)))

	if len(p.Types) == 2 {
		typeStr := p.Types[1].GetName()
		outStr += " / " + lipgloss.NewStyle().Foreground(GetTypeColor(typeStr)).Render(utils.StripAndTitle(typeStr))
	}
	outStr += "\n"

	var defendVals, headers []string
	for _, typeStr := range TYPE_LIST {
		typeStyled := lipgloss.NewStyle().Foreground(GetTypeColor(typeStr)).Render(strings.ToUpper(typeStr[0:3]))
		headers = append(headers, typeStyled)
	}

	for _, typeStr := range TYPE_LIST {
		attackType, ok := cache.Get(internal.Type, typeStr)
		if !ok {
			defendVals = append(defendVals, "?")

		} else {
			attack, _ := attackType.(*Type)
			defendVals = append(defendVals, EffectivenessAgainst(attack, p.Types).GetString(true))
		}
	}

	defTable := table.New().Border(lipgloss.RoundedBorder()).Headers(headers...).Row(defendVals...)

	defenseHeader := lipgloss.NewStyle().AlignHorizontal(lipgloss.Center).Width(16).Bold(true).Render("~ Type Defense ~")

	defenseOut := lipgloss.JoinVertical(lipgloss.Center, defenseHeader, defTable.Render())

	outStr = lipgloss.JoinVertical(lipgloss.Center, outStr, defenseOut)

	return outStr

}

// Region: API Access Stuff

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

type pokemonSpeciesAPIResponse struct {
	BaseHappiness int               `json:"base_happiness,omitempty"`
	CaptureRate   int               `json:"capture_rate,omitempty"`
	Color         api.RespPointer   `json:"color"`
	EggGroups     []api.RespPointer `json:"egg_groups,omitempty"`
	EvolvesFrom   string            `json:"evolves_from,omitempty"`
	GenderRatio   int               `json:"gender_ratio,omitempty"`

	Generation api.RespPointer `json:"generation"`
	GrowthRate api.RespPointer `json:"growth_rate"`
	Habitat    api.RespPointer `json:"habitat"`

	HasGenderDifferences bool `json:"has_gender_differences,omitempty"`

	HatchCounter int `json:"hatch_counter,omitempty"`

	IsBaby      bool `json:"is_baby,omitempty"`
	IsLegendary bool `json:"is_legendary,omitempty"`
	IsMythical  bool `json:"is_mythical,omitempty"`

	PokedexNumbers []struct {
		EntryNumber int             `json:"entry_number,omitempty"`
		Pokedex     api.RespPointer `json:"pokedex"`
	} `json:"pokedex_numbers,omitempty"`

	Shape api.RespPointer `json:"shape"`
}

func init() {
	internal.RegisterLoader(internal.Pokemon, func(url string) (internal.Resource, error) {
		data, err := api.QueryAndUnmarshal[pokemonAPIResponse](url)
		if err != nil {
			return nil, err
		}

		speciesData, err := api.QueryAndUnmarshal[pokemonSpeciesAPIResponse](data.Species.URL)
		if err != nil {
			return nil, err
		}

		p := &Pokemon{
			Name:    data.Name,
			URL:     url,
			ID:      data.ID,
			Kind:    internal.Pokemon,
			BaseExp: data.BaseExperience,

			BaseHappiness: speciesData.BaseHappiness,
			CaptureRate:   speciesData.CaptureRate,
			Color:         speciesData.Color.Name,
			GenderRatio:   speciesData.GenderRatio,
			Habitat:       speciesData.Habitat.Name,
			HatchCounter:  speciesData.HatchCounter,
			IsBaby:        speciesData.IsBaby,
			IsLegendary:   speciesData.IsLegendary,
			IsMythical:    speciesData.IsMythical,
			Shape:         speciesData.Shape.Name,

			Height:       data.Height,
			Weight:       data.Weight,
			CryLatestURL: data.Cries.Latest,
			CryLegacyURL: data.Cries.Legacy,
			LocEncURL:    data.LocationAreaEncounters,
			Sprites:      make(map[string]string),
			// Response:     data,
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
