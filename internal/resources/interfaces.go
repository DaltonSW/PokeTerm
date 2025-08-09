package resources

// Characteristic, ContestEffect, EvolutionChain, Machine, and SuperContestEffect are the only unnamed resources
type Resource interface {
	GetURL() string
	QueryURL() []byte
}

// Every resource not mentioned above has a name
type NamedResource interface {
	Resource
	GetName() string
}

// Berries
//	Berry
//	Berry Firmness
//	Berry Flavor

// Contests
//	Contest Type
//	Contest Name
//	Contest Effect
//	Super Contest Effect

// Encounters
//	Encounter Method
//	Encounter Conditions
//	Encounter Condition Value

// Evolution
//	Evolution Chain
//	Chain Link
//	Evolution Detail
//	Evolution Trigger

// Games
//	Generations
//	Pokedex
//	Pokemon Entry
//	Version
//	Version Group

// Items
//	Item
//	Item Sprite
//	Item Holder Pokemon
//	Item Holder Pokemon Version Detail
//	Item Attribute
//	Item Category
//	Item Fling Effect
//	Item Pocket

// Locations
//	Location
//	Location Area
//	Encounter Method Rate
//	Encounter Version Details
//	Pokemon Encounter
//	Pal Park Area
//	Pal Park Encounter Species
//	Region

// Machines
//	Machine

// Moves
//	Move
//	Contest Combo Sets
//	Contest Combo Detail
//	Move Flavor Test
//	Move Metadata
//	Move Stat Change
//	Past Move Stat Values
//	Move Ailment
//	Move Battle Style
//	Move Category
//	Move Damage Class
//	Move Learn Method
//	Move Target

// Pokemon
//	Ability
//	Ability Effect Change
//	Ability Flavor Text
//	Ability Pokemon
//	Characteristic
//	Egg Group
//	Gender
//	Pokemon Species Gender
//	Growth Rate
//	Growth Rate Exp. Level
//	Nature
//	Nature Stat Change
//	Move Battle Style Preference
//	Pokeathlon Stat
//	Nature Pokeathlon Stat Affect Sets
//	Nature Pokeathlon Stat Affect
//	Pokemon
//	Pokemon Ability
//	Pokemon Type
//	Pokemon Form Type
//	Pokemon Type Past
//	Pokemon Ability Past
//	Pokemon Held Item
//	Pokemon Held Item Version
//	Pokemon Move
//	Pokemon Move Version
//	Pokemon Stat
//	Pokemon Sprites
//	Pokemon Cries
//	Location Area Encounter
//	Pokemon Color
//	Pokemon Form
//	Pokemon Form Sprites
//	Pokemon Habitat
//	Pokemon Shape
//	Awesome Name
//	Pokemon Species
//	Genus
//	Pokemon Species Dex Entry
//	Pal Park Encounter Area
//	Pokemon Species Variety
//	Stat
//	Move Stat Affect Sets
//	Move Stat Affect
//	Nature Stat Affect Sets
//	Type
//	Type Pokemon
//	Type Relations
