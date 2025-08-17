package resources

import (
	"fmt"

	"go.dalton.dog/poketerm/internal"
	"go.dalton.dog/poketerm/internal/api"
)

type Type struct {
	ID   int
	Name string
	URL  string

	Ref internal.ResourceRef

	// Effectivenesses
	DoubleDamageFrom []*Type
	HalfDamageFrom   []*Type
	DoubleDamageTo   []*Type
	HalfDamageTo     []*Type
	NoDamageFrom     []*Type
	NoDamageTo       []*Type

	// Moves   []*Move
	Pokemon []*Pokemon
}

func (t *Type) GetName() string              { return t.Name }
func (t *Type) GetURL() string               { return t.URL }
func (t *Type) GetRef() internal.ResourceRef { return t.Ref }
func (t *Type) GetRelated() []internal.ResourceRef {
	var refs []internal.ResourceRef

	// Add Pokemon refs
	for _, p := range t.Pokemon {
		refs = append(refs, internal.ResourceRef{
			Name: p.GetName(), URL: p.URL, Kind: internal.Pokemon, // Use constant
		})
	}

	// Helper function to add damage relation type refs
	addDamageTypeRefs := func(types []*Type) {
		for _, relatedType := range types {
			refs = append(refs, internal.ResourceRef{
				Name: relatedType.Name, URL: relatedType.URL, Kind: internal.Type, // Use constant
			})
		}
	}

	// Add Damage Relation Type refs
	addDamageTypeRefs(t.DoubleDamageFrom)
	addDamageTypeRefs(t.HalfDamageFrom)
	addDamageTypeRefs(t.DoubleDamageTo)
	addDamageTypeRefs(t.HalfDamageTo)
	addDamageTypeRefs(t.NoDamageFrom)
	addDamageTypeRefs(t.NoDamageTo)

	return refs
}

// GetPreview is updated to accept the cache to pull full details if needed
func (t *Type) GetPreview(cache *internal.Cache) string {
	s := fmt.Sprintf("Type: %s (ID: %d)\n\n", t.Name, t.ID)

	s += "Damage Relations:\n"
	if len(t.DoubleDamageFrom) > 0 {
		s += "  Double Damage From: "
		for i, typ := range t.DoubleDamageFrom {
			if i > 0 {
				s += ", "
			}
			if fullType, loaded := cache.Get(internal.Type, typ.GetName()); loaded {
				s += fullType.GetName()
			} else {
				s += fmt.Sprintf("%s (Loading...)", typ.GetName())
			}
		}
		s += "\n"
	}
	if len(t.HalfDamageFrom) > 0 {
		s += "  Half Damage From:   "
		for i, typ := range t.HalfDamageFrom {
			if i > 0 {
				s += ", "
			}
			if fullType, loaded := cache.Get(internal.Type, typ.GetName()); loaded {
				s += fullType.GetName()
			} else {
				s += fmt.Sprintf("%s (Loading...)", typ.GetName())
			}
		}
		s += "\n"
	}
	if len(t.DoubleDamageTo) > 0 {
		s += "  Double Damage To:   "
		for i, typ := range t.DoubleDamageTo {
			if i > 0 {
				s += ", "
			}
			if fullType, loaded := cache.Get(internal.Type, typ.GetName()); loaded {
				s += fullType.GetName()
			} else {
				s += fmt.Sprintf("%s (Loading...)", typ.GetName())
			}
		}
		s += "\n"
	}
	if len(t.HalfDamageTo) > 0 {
		s += "  Half Damage To:     "
		for i, typ := range t.HalfDamageTo {
			if i > 0 {
				s += ", "
			}
			if fullType, loaded := cache.Get(internal.Type, typ.GetName()); loaded {
				s += fullType.GetName()
			} else {
				s += fmt.Sprintf("%s (Loading...)", typ.GetName())
			}
		}
		s += "\n"
	}
	if len(t.NoDamageFrom) > 0 {
		s += "  No Damage From:     "
		for i, typ := range t.NoDamageFrom {
			if i > 0 {
				s += ", "
			}
			if fullType, loaded := cache.Get(internal.Type, typ.GetName()); loaded {
				s += fullType.GetName()
			} else {
				s += fmt.Sprintf("%s (Loading...)", typ.GetName())
			}
		}
		s += "\n"
	}
	if len(t.NoDamageTo) > 0 {
		s += "  No Damage To:       "
		for i, typ := range t.NoDamageTo {
			if i > 0 {
				s += ", "
			}
			if fullType, loaded := cache.Get(internal.Type, typ.GetName()); loaded {
				s += fullType.GetName()
			} else {
				s += fmt.Sprintf("%s (Loading...)", typ.GetName())
			}
		}
		s += "\n"
	}

	s += fmt.Sprintf("\nPokémon Count: %d\n", len(t.Pokemon))
	// Add some Pokémon names for preview if desired, with loading states
	for i, p := range t.Pokemon {
		if i >= 3 { // Limit to 3 for brevity in preview
			s += "  ...\n"
			break
		}
		if fullPokemon, loaded := cache.Get(internal.Pokemon, p.GetName()); loaded {
			s += fmt.Sprintf("  - %s (Loaded)\n", fullPokemon.GetName())
		} else {
			s += fmt.Sprintf("  - %s (Loading...)\n", p.GetName())
		}
	}

	return s
}

// TODO:
//	Type Name
//	Effectiveness charts
//	Moves
//	Pokemon (Primary)
//	Pokemon (Secondary)

type typeAPIResponse struct {
	ID   int    `json:"id"`
	Name string `json:"name"`

	DamageRelations struct {
		DoubleDamageFrom []struct {
			Name string `json:"name"`
			URL  string `json:"url"`
		} `json:"double_damage_from,omitempty"`
		DoubleDamageTo []struct {
			Name string `json:"name"`
			URL  string `json:"url"`
		} `json:"double_damage_to,omitempty"`
		HalfDamageFrom []struct {
			Name string `json:"name"`
			URL  string `json:"url"`
		} `json:"half_damage_from,omitempty"`
		HalfDamageTo []struct {
			Name string `json:"name"`
			URL  string `json:"url"`
		} `json:"half_damage_to,omitempty"`
		NoDamageFrom []struct {
			Name string `json:"name"`
			URL  string `json:"url"`
		} `json:"no_damage_from,omitempty"`
		NoDamageTo []struct {
			Name string `json:"name"`
			URL  string `json:"url"`
		} `json:"no_damage_to,omitempty"`
	} `json:"damage_relations"`

	Pokemon []struct {
		Pokemon struct {
			Name string `json:"name"`
			URL  string `json:"url"`
		} `json:"pokemon"`
	} `json:"pokemon"`
}

func init() {
	internal.RegisterLoader(internal.Type, func(url string) (internal.Resource, error) { // Use constant
		data, err := api.QueryAndUnmarshal[typeAPIResponse](url)
		if err != nil {
			return nil, err
		}
		t := &Type{Name: data.Name, URL: url, ID: data.ID}

		// Populate Pokemon
		for _, p := range data.Pokemon {
			t.Pokemon = append(t.Pokemon, &Pokemon{
				Name: p.Pokemon.Name,
				URL:  p.Pokemon.URL,
			})
		}

		// Populate Damage Relations
		for _, rel := range data.DamageRelations.DoubleDamageFrom {
			t.DoubleDamageFrom = append(t.DoubleDamageFrom, &Type{Name: rel.Name, URL: rel.URL})
		}
		for _, rel := range data.DamageRelations.HalfDamageFrom {
			t.HalfDamageFrom = append(t.HalfDamageFrom, &Type{Name: rel.Name, URL: rel.URL})
		}
		for _, rel := range data.DamageRelations.DoubleDamageTo {
			t.DoubleDamageTo = append(t.DoubleDamageTo, &Type{Name: rel.Name, URL: rel.URL})
		}
		for _, rel := range data.DamageRelations.HalfDamageTo {
			t.HalfDamageTo = append(t.HalfDamageTo, &Type{Name: rel.Name, URL: rel.URL})
		}
		for _, rel := range data.DamageRelations.NoDamageFrom {
			t.NoDamageFrom = append(t.NoDamageFrom, &Type{Name: rel.Name, URL: rel.URL})
		}
		for _, rel := range data.DamageRelations.NoDamageTo {
			t.NoDamageTo = append(t.NoDamageTo, &Type{Name: rel.Name, URL: rel.URL})
		}

		return t, nil
	})
}
