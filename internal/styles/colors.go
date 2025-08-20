package styles

import (
	cat "github.com/catppuccin/go"

	"github.com/charmbracelet/lipgloss/v2"
	"github.com/charmbracelet/lipgloss/v2/compat"
)

// Basically all of these colors are taken from either catppuccin or Bulbapedia's Color Templates page
//	URL: https://bulbapedia.bulbagarden.net/wiki/Help:Color_templates

// Catppuccin Theme References
var (
	CatDark  = cat.Mocha
	CatLight = cat.Latte
)

// General Program Colors
var (
	BorderColor = compat.AdaptiveColor{
		Dark:  CatDark.Rosewater(),
		Light: CatLight.Rosewater(),
	}

	DescColor = compat.AdaptiveColor{
		Dark:  CatDark.Overlay1(),
		Light: CatLight.Overlay1(),
	}

	ForeColor = compat.AdaptiveColor{
		Dark:  CatDark.Text(),  // #CDD6F4
		Light: CatLight.Text(), // #4C4F69
	}

	CurrColor = compat.AdaptiveColor{
		Dark:  CatDark.Blue(),
		Light: CatLight.Blue(),
	}
)

// Stat Colors
var (
	AttackColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#F5DE69"),
		Light: lipgloss.Color("#9B8510"),
	}
	DefenseColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#F09A65"),
		Light: lipgloss.Color("#97410C"),
	}
	HealthColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#9EE865"),
		Light: lipgloss.Color("#448F0C"),
	}
	SpAttackColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#66D8F6"),
		Light: lipgloss.Color("#0D7F9D"),
	}
	SpDefenseColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#899EEA"),
		Light: lipgloss.Color("#304591"),
	}
	SpeedColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#E46CCA"),
		Light: lipgloss.Color("#8B1370"),
	}
)

// Contest conditions
var (
	BeautyColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#6DB9D6"),
		Light: lipgloss.Color("#14607D"),
	}
	ClevernessColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#67C282"),
		Light: lipgloss.Color("#0E6929"),
	}
	CoolnessColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#E3765C"),
		Light: lipgloss.Color("#8A1D03"),
	}
	CutenessColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#E286B5"),
		Light: lipgloss.Color("#892D5C"),
	}
	ToughnessColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#DEC240"),
		Light: lipgloss.Color("#856900"),
	}
)

// Characters
var (
	AlderColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#F0AC92"),
		Light: lipgloss.Color("#975339"),
	}
	CynthiaColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#8F8F8F"),
		Light: lipgloss.Color("#353535"),
	}
)

// Egg Groups
var (
	MonsterColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#BBA38B"),
		Light: lipgloss.Color("#624A31"),
	}
	Water1Color = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#9FE1FB"),
		Light: lipgloss.Color("#4688A2"),
	}
	BugColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#C8D775"),
		Light: lipgloss.Color("#6F7E1B"),
	}
	FlyingColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#B7CBF6"),
		Light: lipgloss.Color("#5E7290"),
	}
	FieldColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#EED29B"),
		Light: lipgloss.Color("#957942"),
	}
	FairyColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#FFC0D2"),
		Light: lipgloss.Color("#A66778"),
	}
	GrassColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#AEE294"),
		Light: lipgloss.Color("#55893B"),
	}
	HumanLikeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#87D0CA"),
		Light: lipgloss.Color("#2E7771"),
	}
	Water3Color = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#6FA3CE"),
		Light: lipgloss.Color("#164975"),
	}
	MineralColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#BBB79C"),
		Light: lipgloss.Color("#625E43"),
	}
	AmorphousColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#C1AEDE"),
		Light: lipgloss.Color("#675585"),
	}
	Water2Color = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#8AB9F3"),
		Light: lipgloss.Color("#31609A"),
	}
	DittoColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#D0C8E4"),
		Light: lipgloss.Color("#766F8A"),
	}
	DragonColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#9692D5"),
		Light: lipgloss.Color("#3D397C"),
	}
	NoEggsDiscoveredColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#F5E059"),
		Light: lipgloss.Color("#9B8700"),
	}
)

// Core series games
var (
	RedColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#E77E66"),
		Light: lipgloss.Color("#8E250D"),
	}
	GreenColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#71C671"),
		Light: lipgloss.Color("#176D17"),
	}
	BlueColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#778DE6"),
		Light: lipgloss.Color("#1E348C"),
	}
	YellowColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#FFE57A"),
		Light: lipgloss.Color("#A68C21"),
	}
	GoldColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#E7C46E"),
		Light: lipgloss.Color("#8E6B15"),
	}
	SilverColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#D6D6D6"),
		Light: lipgloss.Color("#7D7D7D"),
	}
	CrystalColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#8CE6FF"),
		Light: lipgloss.Color("#338DA6"),
	}
	RubyColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#DF6F7C"),
		Light: lipgloss.Color("#851623"),
	}
	SapphireColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#818FC6"),
		Light: lipgloss.Color("#28356D"),
	}
	EmeraldColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#59BB8F"),
		Light: lipgloss.Color("#006235"),
	}
	FireRedColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#F6955A"),
		Light: lipgloss.Color("#9D3C01"),
	}
	LeafGreenColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#C1E859"),
		Light: lipgloss.Color("#678F00"),
	}
	DiamondColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#B7D5F3"),
		Light: lipgloss.Color("#5E7C9A"),
	}
	PearlColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#E9AACC"),
		Light: lipgloss.Color("#905173"),
	}
	PlatinumColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#C1C1B5"),
		Light: lipgloss.Color("#68685C"),
	}
	HeartGoldColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#F0CF5B"),
		Light: lipgloss.Color("#977601"),
	}
	SoulSilverColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#C8D2E0"),
		Light: lipgloss.Color("#6F7887"),
	}
	BlackColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#858585"),
		Light: lipgloss.Color("#2C2C2C"),
	}
	WhiteColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#EBEBEB"),
		Light: lipgloss.Color("#929292"),
	}
	Black2Color = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#78828E"),
		Light: lipgloss.Color("#1F2835"),
	}
	White2Color = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#F2D9D8"),
		Light: lipgloss.Color("#99807F"),
	}
	XColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#5A96C5"),
		Light: lipgloss.Color("#013D6C"),
	}
	YColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#F16A81"),
		Light: lipgloss.Color("#981128"),
	}
	OmegaRubyColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#C87365"),
		Light: lipgloss.Color("#6F1A0C"),
	}
	AlphaSapphireColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#729ABF"),
		Light: lipgloss.Color("#194166"),
	}
	SunColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#F6B775"),
		Light: lipgloss.Color("#9D5E1C"),
	}
	MoonColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#90BDDC"),
		Light: lipgloss.Color("#376483"),
	}
	UltraSunColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#F19475"),
		Light: lipgloss.Color("#983B1C"),
	}
	UltraMoonColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#6FA0CF"),
		Light: lipgloss.Color("#164776"),
	}
	LetsGoPikachuColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#F8E772"),
		Light: lipgloss.Color("#9F8E19"),
	}
	LetsGoEeveeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#E3B88A"),
		Light: lipgloss.Color("#8A5F31"),
	}
	SwordColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#59C2F1"),
		Light: lipgloss.Color("#006998"),
	}
	ShieldColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#D5598C"),
		Light: lipgloss.Color("#7C0033"),
	}
	IsleOfArmorColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#FDE060"),
		Light: lipgloss.Color("#A48707"),
	}
	CrownTundraColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#66CA9C"),
		Light: lipgloss.Color("#0D7143"),
	}
	BrilliantDiamondColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#85D2EE"),
		Light: lipgloss.Color("#2C7995"),
	}
	ShiningPearlColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#E7ABBD"),
		Light: lipgloss.Color("#8E5163"),
	}
	LegendsArceusColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#7C93A9"),
		Light: lipgloss.Color("#233A50"),
	}
	ScarletColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#F7837B"),
		Light: lipgloss.Color("#9E2A22"),
	}
	VioletColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#AE7BD0"),
		Light: lipgloss.Color("#552277"),
	}
	TealMaskColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#59C3BB"),
		Light: lipgloss.Color("#006A62"),
	}
	IndigoDiskColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#5987A7"),
		Light: lipgloss.Color("#002E4E"),
	}
	LegendsZAColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#79DD91"),
		Light: lipgloss.Color("#208338"),
	}
)

// Other games
var (
	ColosseumColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#D0DDED"),
		Light: lipgloss.Color("#768394"),
	}
	XdColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#988CAE"),
		Light: lipgloss.Color("#3E3355"),
	}
	MdColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#E5AD85"),
		Light: lipgloss.Color("#8C542C"),
	}
	MdRedColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#D9618D"),
		Light: lipgloss.Color("#800834"),
	}
	MdBlueColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#5F94CB"),
		Light: lipgloss.Color("#063B72"),
	}
	MdTimeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#6FB7DB"),
		Light: lipgloss.Color("#155E81"),
	}
	MdDarknessColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#D8666B"),
		Light: lipgloss.Color("#7F0D12"),
	}
	MdSkyColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#A9CF8D"),
		Light: lipgloss.Color("#507633"),
	}
	RangerColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#FA9D6A"),
		Light: lipgloss.Color("#A14411"),
	}
	ShadowsOfAlmiaColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#778ABC"),
		Light: lipgloss.Color("#1D3163"),
	}
	GuardianSignsColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#76D1F1"),
		Light: lipgloss.Color("#1D7898"),
	}
	BattleRevolutionColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#E8C35B"),
		Light: lipgloss.Color("#8F6901"),
	}
	MastersColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#A0C6D1"),
		Light: lipgloss.Color("#476D78"),
	}
	CafeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#DFA37D"),
		Light: lipgloss.Color("#854A24"),
	}
	HomeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#59C1A9"),
		Light: lipgloss.Color("#00674F"),
	}
	UniteColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#FCA770"),
		Light: lipgloss.Color("#A34E17"),
	}
	GoColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#5A98CB"),
		Light: lipgloss.Color("#013F72"),
	}
	PocketColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#7D9ACB"),
		Light: lipgloss.Color("#244072"),
	}
	PokemonColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#EE9B80"),
		Light: lipgloss.Color("#954227"),
	}
)

// Regions
var (
	KantoColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#ACD36C"),
		Light: lipgloss.Color("#537A13"),
	}
	JohtoColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#DCD677"),
		Light: lipgloss.Color("#837D1E"),
	}
	HoennColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#9CD7C8"),
		Light: lipgloss.Color("#437E6F"),
	}
	SinnohColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#B7A3C3"),
		Light: lipgloss.Color("#5E4A6A"),
	}
	UnovaColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#9FCADF"),
		Light: lipgloss.Color("#467186"),
	}
	KalosColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#DD608C"),
		Light: lipgloss.Color("#840733"),
	}
	AlolaColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#E89483"),
		Light: lipgloss.Color("#8F3B2A"),
	}
	GalarColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#C97DC0"),
		Light: lipgloss.Color("#702467"),
	}
	HisuiColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#7C93A9"),
		Light: lipgloss.Color("#233A50"),
	}
	PaldeaColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#EBC081"),
		Light: lipgloss.Color("#926828"),
	}
	KitakamiColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#59C3BB"),
		Light: lipgloss.Color("#006A62"),
	}
	BlueberryColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#5987A7"),
		Light: lipgloss.Color("#002E4E"),
	}
	OrangeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#FFAC59"),
		Light: lipgloss.Color("#A65300"),
	}
	OrreColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#ADA588"),
		Light: lipgloss.Color("#544C2F"),
	}
	PokeParkColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#A7DB8D"),
		Light: lipgloss.Color("#4E8234"),
	}
	SeviiColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#8FDEB8"),
		Light: lipgloss.Color("#35855E"),
	}
)

// Video game types
var (
	BugTypeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#B8C26A"),
		Light: lipgloss.Color("#5E6910"),
	}
	DarkTypeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#998B8C"),
		Light: lipgloss.Color("#403233"),
	}
	DragonTypeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#8D98EC"),
		Light: lipgloss.Color("#343E92"),
	}
	ElectricTypeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#FCD659"),
		Light: lipgloss.Color("#A37D00"),
	}
	FairyTypeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#F5A2F5"),
		Light: lipgloss.Color("#9B499B"),
	}
	FightingTypeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#FFAC59"),
		Light: lipgloss.Color("#A65300"),
	}
	FireTypeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#EF7374"),
		Light: lipgloss.Color("#961A1B"),
	}
	FlyingTypeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#ADD2F5"),
		Light: lipgloss.Color("#54789B"),
	}
	GhostTypeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#A284A2"),
		Light: lipgloss.Color("#492A49"),
	}
	GrassTypeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#82C274"),
		Light: lipgloss.Color("#29691B"),
	}
	GroundTypeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#B88E6F"),
		Light: lipgloss.Color("#5E3515"),
	}
	IceTypeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#81DFF7"),
		Light: lipgloss.Color("#28869E"),
	}
	NormalTypeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#C1C2C1"),
		Light: lipgloss.Color("#676967"),
	}
	PoisonTypeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#B884DD"),
		Light: lipgloss.Color("#5E2A84"),
	}
	PsychicTypeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#F584A8"),
		Light: lipgloss.Color("#9B2A4F"),
	}
	RockTypeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#CBC7AD"),
		Light: lipgloss.Color("#726E54"),
	}
	SteelTypeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#98C2D1"),
		Light: lipgloss.Color("#3E6978"),
	}
	StellarTypeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#83CFC5"),
		Light: lipgloss.Color("#2A766B"),
	}
	WaterTypeColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#74ACF5"),
		Light: lipgloss.Color("#1B539B"),
	}
	UnknownTypeColor = compat.AdaptiveColor{ // Changed ??? to Unknown
		Dark:  lipgloss.Color("#9DC1B7"),
		Light: lipgloss.Color("#44685E"),
	}
	UnknownTypeTextColor = lipgloss.Color("#FFFFFF") // Changed ??? to Unknown
)

// Seasons
var (
	SpringColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#C7FA89"),
		Light: lipgloss.Color("#7BAE3D"),
	}
	SummerColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#A0DEFA"),
		Light: lipgloss.Color("#5492AE"),
	}
	AutumnColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#FAB189"),
		Light: lipgloss.Color("#AE653D"),
	}
	WinterColor = compat.AdaptiveColor{
		Dark:  lipgloss.Color("#F4E3FA"),
		Light: lipgloss.Color("#A897AE"),
	}
)

// Effectiveness
var (
	Ineffective = compat.AdaptiveColor{
		Dark:  CatDark.Lavender(),
		Light: CatLight.Lavender(),
	}
	QuarterEffective = compat.AdaptiveColor{
		Dark:  CatDark.Red(),
		Light: CatLight.Red(),
	}
	HalfEffective = compat.AdaptiveColor{
		Dark:  CatDark.Maroon(),
		Light: CatLight.Maroon(),
	}
	DoubleEffective = compat.AdaptiveColor{
		Dark:  CatDark.Green(),
		Light: CatLight.Green(),
	}
	QuadEffective = compat.AdaptiveColor{
		Dark:  CatDark.Green(),
		Light: CatLight.Green(),
	}
)
