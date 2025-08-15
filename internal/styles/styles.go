package styles

import (
	"github.com/charmbracelet/lipgloss/v2"
	"github.com/charmbracelet/lipgloss/v2/compat"
)

// Colors
var (
	BorderColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#A8A8A8"), // light gray for dark mode
		Light: lipgloss.Color("#505050"), // dark gray for light mode
	}

	DescColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#505050"),
		Light: lipgloss.Color("#A8A8A8"),
	}

	ForeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#FFFFFF"),
		Light: lipgloss.Color("#000000"),
	}
)

// Type Colors (based on official Pokémon palette)
var (
	NormalColor   = compat.AdaptiveColor{Dark: lipgloss.Color("#A8A77A"), Light: lipgloss.Color("#6D6D4E")}
	FireColor     = compat.AdaptiveColor{Dark: lipgloss.Color("#EE8130"), Light: lipgloss.Color("#B22222")}
	WaterColor    = compat.AdaptiveColor{Dark: lipgloss.Color("#6390F0"), Light: lipgloss.Color("#1E3A8A")}
	ElectricColor = compat.AdaptiveColor{Dark: lipgloss.Color("#F7D02C"), Light: lipgloss.Color("#B8860B")}
	GrassColor    = compat.AdaptiveColor{Dark: lipgloss.Color("#7AC74C"), Light: lipgloss.Color("#2E8B57")}
	IceColor      = compat.AdaptiveColor{Dark: lipgloss.Color("#96D9D6"), Light: lipgloss.Color("#4682B4")}
	FightingColor = compat.AdaptiveColor{Dark: lipgloss.Color("#C22E28"), Light: lipgloss.Color("#8B0000")}
	PoisonColor   = compat.AdaptiveColor{Dark: lipgloss.Color("#A33EA1"), Light: lipgloss.Color("#6A0DAD")}
	GroundColor   = compat.AdaptiveColor{Dark: lipgloss.Color("#E2BF65"), Light: lipgloss.Color("#8B7355")}
	FlyingColor   = compat.AdaptiveColor{Dark: lipgloss.Color("#A98FF3"), Light: lipgloss.Color("#483D8B")}
	PsychicColor  = compat.AdaptiveColor{Dark: lipgloss.Color("#F95587"), Light: lipgloss.Color("#C71585")}
	BugColor      = compat.AdaptiveColor{Dark: lipgloss.Color("#A6B91A"), Light: lipgloss.Color("#556B2F")}
	RockColor     = compat.AdaptiveColor{Dark: lipgloss.Color("#B6A136"), Light: lipgloss.Color("#8B814C")}
	GhostColor    = compat.AdaptiveColor{Dark: lipgloss.Color("#735797"), Light: lipgloss.Color("#4B0082")}
	DragonColor   = compat.AdaptiveColor{Dark: lipgloss.Color("#6F35FC"), Light: lipgloss.Color("#301934")}
	DarkColor     = compat.AdaptiveColor{Dark: lipgloss.Color("#705746"), Light: lipgloss.Color("#3B2F2F")}
	SteelColor    = compat.AdaptiveColor{Dark: lipgloss.Color("#B7B7CE"), Light: lipgloss.Color("#5A5A7A")}
	FairyColor    = compat.AdaptiveColor{Dark: lipgloss.Color("#D685AD"), Light: lipgloss.Color("#A0527D")}
)

// Stat Colors
var (
	AttackColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#FF4500"), // orange-red
		Light: lipgloss.Color("#B22222"), // dark red
	}
	DefenseColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#1E90FF"), // dodger blue
		Light: lipgloss.Color("#00008B"), // dark blue
	}
	SpAttackColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#FF69B4"), // hot pink
		Light: lipgloss.Color("#C71585"), // medium violet red
	}
	SpDefenseColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#32CD32"), // lime green
		Light: lipgloss.Color("#006400"), // dark green
	}
	SpeedColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#FFD700"), // gold
		Light: lipgloss.Color("#B8860B"), // dark goldenrod
	}
	HealthColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#FF0000"), // red
		Light: lipgloss.Color("#8B0000"), // dark red
	}
)

// Resource Type Colors
var (
	PokemonResColor = compat.AdaptiveColor{Dark: lipgloss.Color("#EE8130"), Light: lipgloss.Color("#B22222")}
	AbilityResColor = compat.AdaptiveColor{Dark: lipgloss.Color("#6390F0"), Light: lipgloss.Color("#1E3A8A")}
	TypeResColor    = compat.AdaptiveColor{Dark: lipgloss.Color("#F7D02C"), Light: lipgloss.Color("#B8860B")}
	MoveResColor    = compat.AdaptiveColor{Dark: lipgloss.Color("#7AC74C"), Light: lipgloss.Color("#2E8B57")}
	// PokemonResourceColor = compat.AdaptiveColor{Dark: lipgloss.Color(""), Light: lipgloss.Color("")}
)

type ListStyles struct {
	Title lipgloss.Style
	Desc  lipgloss.Style
	Curr  lipgloss.Style
}

func GetListStyles() ListStyles {
	return ListStyles{
		Title: lipgloss.NewStyle().Foreground(AttackColor),
		Desc:  lipgloss.NewStyle().Foreground(DescColor).Italic(true),
		Curr:  lipgloss.NewStyle().Foreground(DefenseColor),
	}
}
