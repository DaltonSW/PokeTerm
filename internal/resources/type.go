package resources

import "go.dalton.dog/poketerm/internal/api"

type Type struct {
	ID      int
	Name    string
	URL     string
	Pokemon []*Pokemon
}

func (t *Type) GetName() string { return t.Name }
func (t *Type) GetURL() string  { return t.URL }
func (t *Type) GetRelated() []ResourceRef {
	var refs []ResourceRef
	for _, p := range t.Pokemon {
		refs = append(refs, ResourceRef{
			Name: p.Name, URL: p.URL, Kind: "pokemon",
		})
	}
	return refs
}

type typeAPIResponse struct {
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
	RegisterLoader("type", func(url string) (Resource, error) {
		data, err := api.QueryAndUnmarshal[typeAPIResponse](url)
		if err != nil {
			return nil, err
		}
		t := &Type{Name: data.Name, URL: url, ID: data.ID}
		for _, p := range data.Pokemon {
			t.Pokemon = append(t.Pokemon, &Pokemon{
				Name: p.Pokemon.Name,
				URL:  p.Pokemon.URL,
			})
		}
		return t, nil
	})
}
