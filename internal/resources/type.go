package resources

import (
	"fmt"
	"image/color"
	"strings"

	"github.com/charmbracelet/lipgloss/v2"
	"github.com/charmbracelet/lipgloss/v2/compat"
	"github.com/charmbracelet/lipgloss/v2/table"
	"go.dalton.dog/poketerm/internal"
	"go.dalton.dog/poketerm/internal/api"
	"go.dalton.dog/poketerm/internal/styles"
	"go.dalton.dog/poketerm/internal/utils"
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

func (eff TypeEffectiveness) GetString(defending bool) string {
	var str string
	var color compat.AdaptiveColor
	switch eff {
	case Ineffective:
		str = "0x"
		color = utils.Ternary(defending, styles.DoubleEffective, styles.Ineffective)
	case QuarterEffective:
		str = "¼x"
		color = utils.Ternary(defending, styles.DoubleEffective, styles.QuarterEffective)
	case HalfEffective:
		// str = "1/2x"
		str = "½x"
		color = utils.Ternary(defending, styles.DoubleEffective, styles.HalfEffective)
	case DoubleEffective:
		str = "2x"
		color = utils.Ternary(defending, styles.HalfEffective, styles.DoubleEffective)
	case QuadEffective:
		str = "4x"
		color = utils.Ternary(defending, styles.QuarterEffective, styles.QuadEffective)
	default:
		str = "1x"
		color = styles.ForeColor
	}

	return lipgloss.NewStyle().Width(3).Foreground(color).Render(str)
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

	mainAreaHeight int
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

	return refs
}

// GetPreview is updated to accept the cache to pull full details if needed
func (t *Type) GetPreview(cache *internal.Cache, width, height int) string {
	title := lipgloss.NewStyle().MaxWidth(width).
		Foreground(GetTypeColor(t.Name)).
		Bold(true).Italic(true).Underline(true).
		AlignHorizontal(lipgloss.Center).
		Render(utils.StripAndTitle(t.Name) + "\n")

	sTypes := lipgloss.NewStyle().MaxWidth(width).Padding(0, 1, 1).Render(t.typeInfo())

	mainAreaHeight := height - lipgloss.Height(title) - lipgloss.Height(sTypes) - 1

	mainView := lipgloss.NewStyle().
		Width(lipgloss.Width(sTypes) / 2).MaxHeight(mainAreaHeight).Height(mainAreaHeight).
		Border(lipgloss.RoundedBorder()).BorderForeground(GetTypeColor(t.Name)).
		Align(lipgloss.Left)

	sPokes := internal.ResourceToList(t.Pokemon, mainAreaHeight-mainView.GetVerticalFrameSize(), cache, true)
	sMoves := internal.ResourceToList(t.Moves, mainAreaHeight-mainView.GetVerticalFrameSize(), cache, true)

	headerStyle := lipgloss.NewStyle().AlignHorizontal(lipgloss.Center).
		Width(mainView.GetWidth()).Bold(true)

	pokesHeader := headerStyle.Render(fmt.Sprintf("~ Pokemon (%v) ~", len(t.Pokemon)))
	movesHeader := headerStyle.Render(fmt.Sprintf("~ Moves (%v) ~", len(t.Moves)))

	pokesHalf := lipgloss.JoinVertical(lipgloss.Center, pokesHeader, mainView.Render(sPokes.String()))
	movesHalf := lipgloss.JoinVertical(lipgloss.Center, movesHeader, mainView.Render(sMoves.String()))

	sView := lipgloss.JoinHorizontal(lipgloss.Top, movesHalf, pokesHalf)

	return lipgloss.JoinVertical(lipgloss.Center, title, sTypes, sView)
}

func (t Type) typeInfo() string {

	var attackVals, defendVals, headers []string
	for _, typeStr := range TYPE_LIST {
		typeStyled := lipgloss.NewStyle().Foreground(GetTypeColor(typeStr)).Render(strings.ToUpper(typeStr[0:3]))
		headers = append(headers, typeStyled)
	}

	for _, typeStr := range TYPE_LIST {
		attackVals = append(attackVals, t.AttackingDamageRatios[typeStr].GetString(false))
		defendVals = append(defendVals, t.DefendingDamageRatios[typeStr].GetString(false))
	}

	attackTable := table.New().Border(lipgloss.RoundedBorder()).Headers(headers...).Row(attackVals...)
	defTable := table.New().Border(lipgloss.RoundedBorder()).Headers(headers...).Row(defendVals...)

	attackHeader := lipgloss.NewStyle().AlignHorizontal(lipgloss.Center).Width(16).Bold(true).Render("~ Attack ~")
	defenseHeader := lipgloss.NewStyle().AlignHorizontal(lipgloss.Center).Width(16).Bold(true).Render("~ Defend ~")

	attackOut := lipgloss.JoinVertical(lipgloss.Center, attackHeader, attackTable.Render())
	defenseOut := lipgloss.JoinVertical(lipgloss.Center, defenseHeader, defTable.Render())

	return lipgloss.JoinVertical(lipgloss.Center, attackOut, defenseOut)
	// return lipgloss.JoinHorizontal(lipgloss.Top, attackOut, "   ", defenseOut)

}

// GetColor returns a lipgloss.Color based on the type's name.
func GetTypeColor(typeName string) color.Color {
	// Convert name to lowercase to ensure consistent matching
	typeName = strings.ToLower(typeName)

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
