package resources

import "go.dalton.dog/poketerm/internal/api"

type Ability struct {
	ID      int
	Name    string
	URL     string
	Pokemon []*Pokemon
}

func (a *Ability) GetName() string { return a.Name }
func (a *Ability) GetURL() string  { return a.URL }
func (a *Ability) GetRelated() []ResourceRef {
	var refs []ResourceRef
	for _, p := range a.Pokemon {
		refs = append(refs, ResourceRef{
			Name: p.Name, URL: p.URL, Kind: "pokemon",
		})
	}
	return refs
}

type abilityAPIResponse struct {
	ID      int    `json:"id"`
	Name    string `json:"name"`
	Pokemon []struct {
		Pokemon struct {
			Name string `json:"name"`
			URL  string `json:"url"`
		} `json:"pokemon"`
	} `json:"pokemon"`
}

func init() {
	RegisterLoader("ability", func(url string) (Resource, error) {
		data, err := api.QueryAndUnmarshal[abilityAPIResponse](url)
		if err != nil {
			return nil, err
		}
		a := &Ability{Name: data.Name, URL: url, ID: data.ID}
		for _, p := range data.Pokemon {
			a.Pokemon = append(a.Pokemon, &Pokemon{
				Name: p.Pokemon.Name,
				URL:  p.Pokemon.URL,
			})
		}
		return a, nil
	})
}
