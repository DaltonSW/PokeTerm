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

type TypeEffectiveness int

const (
	Ineffective TypeEffectiveness = iota
	QuarterEffective
	HalfEffective
	NormalEffective
	DoubleEffective
	QuadEffective
)

func (eff TypeEffectiveness) GetString() string {
	switch eff {
	case Ineffective:
		return "0x"
	case QuarterEffective:
		return "1/4x"
	case HalfEffective:
		return "1/2x"
	case NormalEffective:
		return "1x"
	case DoubleEffective:
		return "2x"
	case QuadEffective:
		return "4x"
	default:
		return "1x"
	}
}

var TYPE_LIST = []string{"normal", "fire", "water", "grass", "electric", "ice", "fighting", "poison", "ground", "flying", "psychic",
	"bug", "rock", "ghost", "dragon", "steel", "dark", "fairy"}

type Type struct {
	ID   int
	Name string
	URL  string
	Kind internal.ResKind

	// Effectivenesses
	AttackingDamageRatios map[string]TypeEffectiveness
	DefendingDamageRatios map[string]TypeEffectiveness

	DoubleDamageFrom []*Type
	HalfDamageFrom   []*Type
	DoubleDamageTo   []*Type
	HalfDamageTo     []*Type
	NoDamageFrom     []*Type
	NoDamageTo       []*Type

	Pokemon []*Pokemon
	Moves   []*Move
}

func (t *Type) GetName() string               { return t.Name }
func (t *Type) GetURL() string                { return t.URL }
func (t *Type) GetKind() internal.ResKind     { return t.Kind }
func (t *Type) SetKind(kind internal.ResKind) { t.Kind = kind }
func (t *Type) GetRelated() []internal.ResourceRef {
	var refs []internal.ResourceRef

	// Add Pokemon refs
	for _, p := range t.Pokemon {
		refs = append(refs, internal.ResourceRef{Kind: p.Kind, Name: p.Name, URL: p.URL})
	}

	for _, m := range t.Moves {
		refs = append(refs, internal.ResourceRef{Kind: m.Kind, Name: m.Name, URL: m.URL})
	}

	// // Helper function to add damage relation type refs
	// addDamageTypeRefs := func(types []*Type) {
	// 	for _, relatedType := range types {
	// 		refs = append(refs, relatedType.GetRef())
	// 	}
	// }
	//
	// // Add Damage Relation Type refs
	// addDamageTypeRefs(t.DoubleDamageFrom)
	// addDamageTypeRefs(t.HalfDamageFrom)
	// addDamageTypeRefs(t.DoubleDamageTo)
	// addDamageTypeRefs(t.HalfDamageTo)
	// addDamageTypeRefs(t.NoDamageFrom)
	// addDamageTypeRefs(t.NoDamageTo)

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
		if poke, loaded := cache.Get(p.Kind, p.GetName()); loaded {
			pokeList = append(pokeList, poke.GetName()+" (loaded)")
		} else {
			pokeList = append(pokeList, p.GetName()+" (loading...)")
		}

		if i >= height-viewport.GetVerticalBorderSize()-lipgloss.Height(title)-1 {
			break
		}
	}

	sMid := viewport.Render(list.New(pokeList).String())

	var moveList []string
	for i, m := range t.Moves {
		if move, loaded := cache.Get(m.Kind, m.GetName()); loaded {
			moveList = append(moveList, move.GetName()+" (loaded)")
		} else {
			moveList = append(moveList, m.GetName()+" (loading...)")
		}

		if i >= height-viewport.GetVerticalBorderSize()-lipgloss.Height(title)-1 {
			break
		}
	}
	sRight := viewport.Render(list.New(moveList).String())

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

func getTypeMap() map[string]TypeEffectiveness {
	out := make(map[string]TypeEffectiveness)

	for _, typeStr := range TYPE_LIST {
		out[typeStr] = NormalEffective
	}

	return out
}

func (t Type) typeInfo() string {

	attackTable := table.New().Border(lipgloss.RoundedBorder()).Headers("Type", "Attacking")
	defTable := table.New().Border(lipgloss.RoundedBorder()).Headers("Type", "Defending")

	for _, typeStr := range TYPE_LIST {
		attackTable.Row(strings.ToUpper(typeStr), t.AttackingDamageRatios[typeStr].GetString())
		defTable.Row(strings.ToUpper(typeStr), t.AttackingDamageRatios[typeStr].GetString())

	}

	return defTable.String() + "\n" + attackTable.String()

}

type typeAPIResponse struct {
	ID   int    `json:"id"`
	Name string `json:"name"`

	DamageRelations struct {
		DoubleDamageFrom []api.RespPointer `json:"double_damage_from,omitempty"`
		DoubleDamageTo   []api.RespPointer `json:"double_damage_to,omitempty"`
		HalfDamageFrom   []api.RespPointer `json:"half_damage_from,omitempty"`
		HalfDamageTo     []api.RespPointer `json:"half_damage_to,omitempty"`
		NoDamageFrom     []api.RespPointer `json:"no_damage_from,omitempty"`
		NoDamageTo       []api.RespPointer `json:"no_damage_to,omitempty"`
	} `json:"damage_relations"`

	Pokemon []struct {
		Pokemon api.RespPointer
	} `json:"pokemon"`

	Moves []api.RespPointer `json:"moves"`
}

func init() {
	internal.RegisterLoader(internal.Type, func(url string) (internal.Resource, error) { // Use constant
		data, err := api.QueryAndUnmarshal[typeAPIResponse](url)
		if err != nil {
			return nil, err
		}
		t := &Type{Name: data.Name, URL: url, ID: data.ID, Kind: internal.Type}

		t.AttackingDamageRatios = getTypeMap()
		t.DefendingDamageRatios = getTypeMap()

		// Populate Pokemon
		for _, p := range data.Pokemon {
			t.Pokemon = append(t.Pokemon, &Pokemon{
				Name: p.Pokemon.Name,
				URL:  p.Pokemon.URL,
				Kind: internal.Pokemon,
			})
		}

		// Populate Moves
		for _, m := range data.Moves {
			t.Moves = append(t.Moves, &Move{
				Name: m.Name,
				URL:  m.URL,
				Kind: internal.Move,
			})
		}

		// Defending ratios
		for _, rel := range data.DamageRelations.DoubleDamageFrom {
			// t.DoubleDamageFrom = append(t.DoubleDamageFrom, &Type{Name: rel.Name, URL: rel.URL, Kind: internal.Type})
			t.DefendingDamageRatios[rel.Name] = DoubleEffective
		}
		for _, rel := range data.DamageRelations.HalfDamageFrom {
			// t.HalfDamageFrom = append(t.HalfDamageFrom, &Type{Name: rel.Name, URL: rel.URL, Kind: internal.Type})
			t.DefendingDamageRatios[rel.Name] = HalfEffective
		}
		for _, rel := range data.DamageRelations.NoDamageFrom {
			// t.NoDamageFrom = append(t.NoDamageFrom, &Type{Name: rel.Name, URL: rel.URL, Kind: internal.Type})
			t.DefendingDamageRatios[rel.Name] = Ineffective
		}

		// Attacking ratios
		for _, rel := range data.DamageRelations.DoubleDamageTo {
			// t.DoubleDamageTo = append(t.DoubleDamageTo, &Type{Name: rel.Name, URL: rel.URL, Kind: internal.Type})
			t.AttackingDamageRatios[rel.Name] = DoubleEffective
		}
		for _, rel := range data.DamageRelations.HalfDamageTo {
			// t.HalfDamageTo = append(t.HalfDamageTo, &Type{Name: rel.Name, URL: rel.URL, Kind: internal.Type})
			t.AttackingDamageRatios[rel.Name] = HalfEffective
		}
		for _, rel := range data.DamageRelations.NoDamageTo {
			// t.NoDamageTo = append(t.NoDamageTo, &Type{Name: rel.Name, URL: rel.URL, Kind: internal.Type})
			t.AttackingDamageRatios[rel.Name] = Ineffective
		}

		return t, nil
	})
}
