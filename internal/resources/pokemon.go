package resources

type Pokemon struct {
	URL string

	ID             int
	Name           string
	BaseExperience int
	Height         int
	IsDefault      bool
	Order          int
	Weight         int
	// Abilities []Ability
	// Forms []PokemonForm
	// HeldItems []HeldItem
	// Moves []Move
	// Species PokemonSpecies
}

func (p Pokemon) GetEndpoint() string { return "pokemon" }

func (p Pokemon) GetURL() string { return p.URL }
