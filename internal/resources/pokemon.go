package resources

import "go.dalton.dog/poketerm/internal/api"
import "go.dalton.dog/poketerm/internal"

type Pokemon struct {
	ID        int
	Name      string
	URL       string
	Types     []*Type
	Abilities []*Ability
}

func (p *Pokemon) GetName() string { return p.Name }
func (p *Pokemon) GetURL() string  { return p.URL }
func (p *Pokemon) GetRelated() []internal.ResourceRef {
	var refs []internal.ResourceRef
	for _, t := range p.Types {
		refs = append(refs, internal.ResourceRef{
			Name: t.Name, URL: t.URL, Kind: internal.Type,
		})
	}
	for _, a := range p.Abilities {
		refs = append(refs, internal.ResourceRef{
			Name: a.Name, URL: a.URL, Kind: internal.Ability,
		})
	}
	return refs
}

type pokemonAPIResponse struct {
	ID        int    `json:"id"`
	Name      string `json:"name"`
	Abilities []struct {
		Ability struct {
			Name string `json:"name"`
			URL  string `json:"url"`
		} `json:"ability"`
	} `json:"abilities"`
	Types []struct {
		Type struct {
			Name string `json:"name"`
			URL  string `json:"url"`
		}
	}
}

func init() {
	internal.RegisterLoader(internal.Pokemon, func(url string) (internal.Resource, error) {
		data, err := api.QueryAndUnmarshal[pokemonAPIResponse](url)
		if err != nil {
			return nil, err
		}
		p := &Pokemon{Name: data.Name, URL: url, ID: data.ID}
		for _, a := range data.Abilities {
			p.Abilities = append(p.Abilities, &Ability{
				Name: a.Ability.Name,
				URL:  a.Ability.URL,
			})
		}
		for _, t := range data.Types {
			p.Types = append(p.Types, &Type{
				Name: t.Type.Name,
				URL:  t.Type.URL,
			})
		}
		return p, nil
	})
}
