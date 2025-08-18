package resources

import (
	"go.dalton.dog/poketerm/internal"
	"go.dalton.dog/poketerm/internal/api"
)

type Ability struct {
	ID      int
	Name    string
	URL     string
	Kind    internal.ResKind
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
	return "Ability Preview"
}

type abilityAPIResponse struct {
	ID      int    `json:"id"`
	Name    string `json:"name"`
	Pokemon []struct {
		Pokemon api.RespPointer `json:"pokemon"`
	} `json:"pokemon"`
}

func init() {
	internal.RegisterLoader(internal.Ability, func(url string) (internal.Resource, error) {
		data, err := api.QueryAndUnmarshal[abilityAPIResponse](url)
		if err != nil {
			return nil, err
		}
		a := &Ability{Name: data.Name, URL: url, ID: data.ID}
		for _, p := range data.Pokemon {
			a.Pokemon = append(a.Pokemon, &Pokemon{
				Name: p.Pokemon.Name,
				URL:  p.Pokemon.URL,
				Kind: internal.Pokemon,
			})
		}
		return a, nil
	})
}
