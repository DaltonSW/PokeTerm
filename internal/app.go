package internal

import (
	"fmt"

	"github.com/charmbracelet/bubbles/v2/progress"
	"github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/lipgloss/v2"

	"go.dalton.dog/poketerm/internal/api"
)

var TitleStyle = lipgloss.NewStyle().Bold(true).Foreground(lipgloss.Color("#BADA55")).AlignHorizontal(lipgloss.Center)

const BaseURL = "https://pokeapi.co/api/v2"
const EndpointURL = BaseURL + "/%s"
const IdentifierURL = EndpointURL + "/%s"

type MainModel struct {
	progress         progress.Model
	total            int
	completed        int
	err              error
	typeCache        map[string]*Type
	pokemonCache     map[string]*Pokemon
	abilityCache     map[string]*Ability
	loadingTypes     map[string]struct{}
	loadingPokemon   map[string]struct{}
	loadingAbilities map[string]struct{}
}

func NewModel() (m MainModel) {
	m = MainModel{
		progress:         progress.New(progress.WithDefaultGradient()),
		typeCache:        make(map[string]*Type),
		pokemonCache:     make(map[string]*Pokemon),
		abilityCache:     make(map[string]*Ability),
		loadingTypes:     make(map[string]struct{}),
		loadingPokemon:   make(map[string]struct{}),
		loadingAbilities: make(map[string]struct{}),
	}

	m.total = 1
	m.loadingTypes["fire"] = struct{}{}

	return m
}

func (m MainModel) Init() tea.Cmd {
	return LoadType("https://pokeapi.co/api/v2/type/fire")
}

func (m MainModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmds []tea.Cmd

	switch msg := msg.(type) {

	case typeLoadedMsg:
		// Move from loading → loaded
		delete(m.loadingTypes, msg.Type.Name)
		m.typeCache[msg.Type.Name] = msg.Type
		m.completed++
		m.progress.SetPercent(float64(m.completed) / float64(m.total))

		// Queue Pokémon in this type
		for _, p := range msg.Type.Pokemon {
			m.queuePokemon(p.Name, p.URL, &cmds)
		}

	case pokemonLoadedMsg:
		delete(m.loadingPokemon, msg.Pokemon.Name)
		m.pokemonCache[msg.Pokemon.Name] = msg.Pokemon
		m.completed++
		m.progress.SetPercent(float64(m.completed) / float64(m.total))

		// Queue abilities
		for _, a := range msg.Pokemon.Abilities {
			m.queueAbility(a.Name, a.URL, &cmds)
		}

		// Queue types
		for _, t := range msg.Pokemon.Types {
			m.queueType(t.Name, t.URL, &cmds)
		}

	case abilityLoadedMsg:
		delete(m.loadingAbilities, msg.Ability.Name)
		m.abilityCache[msg.Ability.Name] = msg.Ability
		m.completed++
		m.progress.SetPercent(float64(m.completed) / float64(m.total))

		// Queue Pokémon with this ability
		for _, p := range msg.Ability.Pokemon {
			m.queuePokemon(p.Name, p.URL, &cmds)
		}

	case errMsg:
		m.err = msg
		return m, nil

	case tea.KeyMsg:
		if msg.String() == "q" {
			return m, tea.Quit
		}
	}

	return m, tea.Batch(cmds...)
}

func (m MainModel) View() string {
	if m.err != nil {
		return fmt.Sprintf("Error: %v\n", m.err)
	}

	s := fmt.Sprintf("Progress: %d/%d\n", m.completed, m.total)
	s += m.progress.View() + "\n"

	if m.completed == m.total && m.total > 0 {
		s += "\nAll Pokémon loaded for Fire type!\n"
		s += fmt.Sprintf("Abilities loaded: %d\n", len(m.abilityCache))
		s += fmt.Sprintf("Pokemon loaded: %d\n", len(m.pokemonCache))
		s += fmt.Sprintf("Types loaded: %d\n", len(m.typeCache))
		s += "Press q to quit.\n"
	}

	return s
}

//
// ---------- Domain Types ----------
//

type Pokemon struct {
	ID        int
	Name      string
	URL       string
	Types     []*Type
	Abilities []*Ability
}

type Ability struct {
	ID      int
	Name    string
	URL     string
	Pokemon []*Pokemon
}

type Type struct {
	ID      int
	Name    string
	URL     string
	Pokemon []*Pokemon
}

//
// ---------- API Response Structs ----------
//

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

type pokemonAPIResponse struct {
	ID        int    `json:"id"`
	Name      string `json:"name"`
	Abilities []struct {
		Ability struct {
			Name string `json:"name"`
			URL  string `json:"url"`
		} `json:"ability"`
	} `json:"abilities"`
	Types []struct {
		Type struct {
			Name string `json:"name"`
			URL  string `json:"url"`
		}
	}
}

type abilityAPIResponse struct {
	ID      int    `json:"id"`
	Name    string `json:"name"`
	Pokemon []struct {
		Pokemon struct {
			Name string `json:"name"`
			URL  string `json:"url"`
		} `json:"pokemon"`
	} `json:"pokemon"`
}

//
// ---------- Messages ----------
//

type typeLoadedMsg struct {
	Type *Type
}

type pokemonLoadedMsg struct {
	Pokemon *Pokemon
}

type abilityLoadedMsg struct {
	Ability *Ability
}

type errMsg error

//
// ---------- Load Functions ----------
//

func LoadType(url string) tea.Cmd {
	return func() tea.Msg {
		data, err := api.QueryAndUnmarshal[typeAPIResponse](url)
		if err != nil {
			return errMsg(err)
		}

		t := &Type{Name: data.Name, URL: url, ID: data.ID}
		for _, p := range data.Pokemon {
			t.Pokemon = append(t.Pokemon, &Pokemon{
				Name: p.Pokemon.Name,
				URL:  p.Pokemon.URL,
			})
		}

		return typeLoadedMsg{Type: t}
	}
}

func LoadPokemon(url string) tea.Cmd {
	return func() tea.Msg {
		data, err := api.QueryAndUnmarshal[pokemonAPIResponse](url)
		if err != nil {
			return errMsg(err)
		}

		p := &Pokemon{Name: data.Name, URL: url, ID: data.ID}
		for _, a := range data.Abilities {
			p.Abilities = append(p.Abilities, &Ability{
				Name: a.Ability.Name,
				URL:  a.Ability.URL,
			})
		}

		for _, t := range data.Types {
			p.Types = append(p.Types, &Type{
				Name: t.Type.Name,
				URL:  t.Type.URL,
			})
		}

		return pokemonLoadedMsg{Pokemon: p}
	}
}

func LoadAbility(url string) tea.Cmd {
	return func() tea.Msg {
		data, err := api.QueryAndUnmarshal[abilityAPIResponse](url)
		if err != nil {
			return errMsg(err)
		}

		a := &Ability{Name: data.Name, URL: url, ID: data.ID}

		for _, p := range data.Pokemon {
			a.Pokemon = append(a.Pokemon, &Pokemon{
				Name: p.Pokemon.Name,
				URL:  p.Pokemon.URL,
			})
		}

		return abilityLoadedMsg{Ability: a}
	}
}

func (m *MainModel) queueType(name, url string, cmds *[]tea.Cmd) {
	if _, loaded := m.typeCache[name]; !loaded {
		if _, loading := m.loadingTypes[name]; !loading {
			m.loadingTypes[name] = struct{}{}
			*cmds = append(*cmds, LoadType(url))
			m.total++
		}
	}
}

func (m *MainModel) queuePokemon(name, url string, cmds *[]tea.Cmd) {
	if _, loaded := m.pokemonCache[name]; !loaded {
		if _, loading := m.loadingPokemon[name]; !loading {
			m.loadingPokemon[name] = struct{}{}
			*cmds = append(*cmds, LoadPokemon(url))
			m.total++
		}
	}
}

func (m *MainModel) queueAbility(name, url string, cmds *[]tea.Cmd) {
	if _, loaded := m.abilityCache[name]; !loaded {
		if _, loading := m.loadingAbilities[name]; !loading {
			m.loadingAbilities[name] = struct{}{}
			*cmds = append(*cmds, LoadAbility(url))
			m.total++
		}
	}
}
