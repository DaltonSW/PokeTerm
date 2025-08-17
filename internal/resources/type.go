package resources

import (
	"image/color"
	"strings"

	"github.com/charmbracelet/lipgloss/v2"
	"github.com/charmbracelet/lipgloss/v2/list"
	"github.com/charmbracelet/lipgloss/v2/table"
	"go.dalton.dog/poketerm/internal"
	"go.dalton.dog/poketerm/internal/api"
	"go.dalton.dog/poketerm/internal/styles"
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
		refs = append(refs, p.GetRef())
	}

	// Helper function to add damage relation type refs
	addDamageTypeRefs := func(types []*Type) {
		for _, relatedType := range types {
			refs = append(refs, relatedType.GetRef())
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
func (t *Type) GetPreview(cache *internal.Cache, width, height int) string {
	title := lipgloss.NewStyle().Width(width).
		Foreground(t.GetColor()).
		Bold(true).Italic(true).
		AlignHorizontal(lipgloss.Center).
		Render(t.Name)

	viewport := lipgloss.NewStyle().Width(width / 3).Height(height - lipgloss.Height(title)).Border(lipgloss.RoundedBorder()).Align(lipgloss.Center)

	sLeft := viewport.Render(t.typeInfo())

	var pokeList []string
	for i, p := range t.Pokemon {
		pokeList = append(pokeList, p.GetName())
		if i >= height-viewport.GetVerticalBorderSize()-lipgloss.Height(title)-1 {
			break
		}
	}

	sMid := viewport.Render(list.New(pokeList).String())

	// moveList := make([]string, len(t.Moves))
	// for i, m := range t.Moves {
	// 	moveList[i] = m.GetName()
	// 	if i > height-viewport.GetVerticalBorderSize() {
	// 		break
	// 	}
	// }
	// sRight := viewport.Render(list.New(moveList).String())
	sRight := viewport.Render("Coming soon :)")

	sView := lipgloss.JoinHorizontal(lipgloss.Center, sLeft, sMid, sRight)

	return lipgloss.JoinVertical(lipgloss.Top, title, sView)
}

// GetColor returns a lipgloss.Color based on the type's name.
func (t *Type) GetColor() color.Color {
	// Convert name to lowercase to ensure consistent matching
	typeName := strings.ToLower(t.Name)

	switch typeName {
	case "normal":
		return styles.NormalTypeColor
	case "fire":
		return styles.FireTypeColor
	case "water":
		return styles.WaterTypeColor
	case "grass":
		return styles.GrassTypeColor
	case "electric":
		return styles.ElectricTypeColor
	case "ice":
		return styles.IceTypeColor
	case "fighting":
		return styles.FightingTypeColor
	case "poison":
		return styles.PoisonTypeColor
	case "ground":
		return styles.GroundTypeColor
	case "flying":
		return styles.FlyingTypeColor
	case "psychic":
		return styles.PsychicTypeColor
	case "bug":
		return styles.BugTypeColor
	case "rock":
		return styles.RockTypeColor
	case "ghost":
		return styles.GhostTypeColor
	case "dragon":
		return styles.DragonTypeColor
	case "steel":
		return styles.SteelTypeColor
	case "dark":
		return styles.DarkTypeColor
	case "fairy":
		return styles.FairyTypeColor
	default:
		// Fallback for unknown or unmapped types
		return styles.UnknownTypeColor
	}
}

func (t Type) typeInfo() string {

	table := table.New().
		Headers("TYPE", "DAMAGE")

	return table.Render()

}

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
