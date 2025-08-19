package resources

import (
	"go.dalton.dog/poketerm/internal"
	"go.dalton.dog/poketerm/internal/api"
)

type Move struct {
	ID      int
	Name    string
	URL     string
	Kind    internal.ResKind
	Pokemon []*Pokemon
}

func (m *Move) GetName() string               { return m.Name }
func (m *Move) GetURL() string                { return m.URL }
func (m *Move) GetKind() internal.ResKind     { return m.Kind }
func (m *Move) SetKind(kind internal.ResKind) { m.Kind = kind }
func (m *Move) GetRelated() []internal.ResourceRef {
	var refs []internal.ResourceRef
	// for _, p := range m.Pokemon {
	// 	refs = append(refs, internal.ResourceRef{Name: p.Name, Kind: p.Kind, URL: p.URL})
	// }
	return refs
}

func (m *Move) GetPreview(cache *internal.Cache, width, height int) string {
	return "move Preview"
}

type moveAPIResponse struct {
	ID      int    `json:"id"`
	Name    string `json:"name"`
	Pokemon []struct {
		Pokemon api.RespPointer
	} `json:"learned_by_pokemon"`
}

func init() {
	internal.RegisterLoader(internal.Move, func(url string) (internal.Resource, error) {
		data, err := api.QueryAndUnmarshal[moveAPIResponse](url)
		if err != nil {
			return nil, err
		}
		m := &Move{Name: data.Name, URL: url, ID: data.ID, Kind: internal.Move}
		// for _, p := range data.Pokemon {
		// 	m.Pokemon = append(m.Pokemon, &Pokemon{
		// 		Name: p.Pokemon.Name,
		// 		URL:  p.Pokemon.URL,
		// 		Kind: internal.Pokemon,
		// 	})
		// }
		return m, nil
	})
}
