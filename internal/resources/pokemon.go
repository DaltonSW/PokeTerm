package resources

import (
	"go.dalton.dog/poketerm/internal"
	"go.dalton.dog/poketerm/internal/api"
)

type Pokemon struct {
	ID   int
	Name string
	URL  string
	Kind internal.ResKind

	BaseExp int
	Height  int
	Weight  int

	Types     []*Type
	Abilities []*Ability

	HeldItems []*Item

	// Sprites
	// Cries

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
	return "Pokemon Preview"
}

type pokemonAPIResponse struct {
	ID   int    `json:"id"`
	Name string `json:"name"`

	Abilities []struct {
		Ability  api.RespPointer `json:"ability"`
		IsHidden bool
		Slot     int
	} `json:"abilities"`

	// Order int `json:"order"` // I think this is used for sorting?
	//
	// BaseExperience int
	//
	// Height int
	// Weight int
	//
	// IsDefault bool
	//
	// LocationAreaEncounters string // URL pointing to encounters
	//
	// Cries []struct {
	// 	Latest string
	// 	Legacy string
	// }
	//
	// Forms []api.RespPointer
	//
	// Stats []struct {
	// 	BaseStat int
	// 	Effort   int
	// 	Stat     api.RespPointer
	// }
	//
	// Types []struct {
	// 	Slot int
	// 	Type api.RespPointer
	// }
	//
	// Species api.RespPointer
}

func init() {
	internal.RegisterLoader(internal.Pokemon, func(url string) (internal.Resource, error) {
		data, err := api.QueryAndUnmarshal[pokemonAPIResponse](url)
		if err != nil {
			return nil, err
		}
		p := &Pokemon{Name: data.Name, URL: url, ID: data.ID, Kind: internal.Pokemon}
		for _, a := range data.Abilities {
			p.Abilities = append(p.Abilities, &Ability{
				Name: a.Ability.Name,
				URL:  a.Ability.URL,
				Kind: internal.Ability,
			})
		}
		// for _, t := range data.Types {
		// 	p.Types = append(p.Types, &Type{
		// 		Name: t.Type.Name,
		// 		URL:  t.Type.URL,
		// 		Kind: internal.Type,
		// 	})
		// }
		return p, nil
	})
}
