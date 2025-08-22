package internal

import (
	"fmt"
	"strings"

	tea "github.com/charmbracelet/bubbletea/v2"
	"github.com/charmbracelet/lipgloss/v2"
	"github.com/charmbracelet/lipgloss/v2/list"
	"github.com/charmbracelet/log"

	"go.dalton.dog/poketerm/internal/api"
	"go.dalton.dog/poketerm/internal/utils"
)

type ResKind string

// TODO:
//	Move
//	Berry
//	Game / Generation
//	Location
//	Item

const (
	Pokemon ResKind = "pokemon"
	Type    ResKind = "type"
	Ability ResKind = "ability"
	Move    ResKind = "move"
	// Berry   ResKind = "berry"
)

func ResourceToList[T Resource](resources []T, maxCount int, cache *Cache) *list.List {
	var resList []string
	for i, r := range resources {
		if poke, loaded := cache.Get(r.GetKind(), r.GetName()); loaded {
			resList = append(resList, utils.StripAndTitle(poke.GetName()))
		} else {
			resList = append(resList, lipgloss.NewStyle().Italic(true).Render(utils.StripAndTitle(r.GetName())))
		}

		// 3 to account for display frame and the item we're adding now. It's a little fudy
		if i > maxCount-3 {
			resList = append(resList, fmt.Sprintf("(%v remaining ...)", len(resources)-i))
			break
		}
	}
	return list.New(resList)
}

func (k ResKind) Icon() string {
	switch k {
	case Pokemon:
		return "󰐝"
	case Type:
		return ""
	case Ability:
		return ""
	// case Move:
	// 	return "󰓥"
	default:
		return " "
	}
}

// Resource is an interface representing a given 'thing' that can be
// loaded, viewed, and potentially link out to other Resources
type Resource interface {
	GetName() string
	GetURL() string
	GetKind() ResKind
	SetKind(ResKind)

	GetRelated() []ResourceRef

	// Populate the right half of the screen
	GetPreview(*Cache, int, int) string

	// TODO: GetFullModel() tea.Model
	//	If the list can be made thin enough, maybe this can be the same as above, just different size?
}

// ResourceRef is just a reference to a given resource on PokeAPI.
// Much smaller than actual resources, these enable providing inital info without
// needing to pre-load a ton of data.
type ResourceRef struct {
	Name string
	URL  string
	Kind ResKind
}

func (ref ResourceRef) Title() string       { return strings.ReplaceAll(ref.Name, "-", " ") }
func (ref ResourceRef) Description() string { return strings.ReplaceAll(string(ref.Kind), "-", " ") }
func (ref ResourceRef) FilterValue() string { return ref.Name }

// LoaderFunc is a type of function that will, for a given ResKind, turn a URL into a Resource.
// The expectation is that each Resource will call RegisterLoader() in their init() function.
type LoaderFunc func(url string) (Resource, error)

var loaders = map[ResKind]LoaderFunc{}

func RegisterLoader(kind ResKind, loader LoaderFunc) {
	loaders[kind] = loader
}

// BubbleTea Messages

// Response to query for references
type getRefsResponse struct {
	Count   int `json:"count"`
	Results []struct {
		Name string `json:"name"`
		URL  string `json:"url"`
	} `json:"results"`
}

// BubbleTea message indicating references have been loaded for a given ResKind
type RefsLoadedMsg struct {
	Kind ResKind
	Refs []ResourceRef
}

// Command to load all references for a given ResKind/endpoint
func LoadRefsCmd(kind ResKind) tea.Cmd {
	return func() tea.Msg {
		url := fmt.Sprintf("%s/%s?limit=2000", BaseURL, string(kind))
		data, err := api.QueryAndUnmarshal[getRefsResponse](url)
		if err != nil {
			return ErrMsg(err)
		}
		refs := make([]ResourceRef, len(data.Results))
		for i, r := range data.Results {
			refs[i] = ResourceRef{Name: r.Name, URL: r.URL, Kind: kind}
		}
		return RefsLoadedMsg{Kind: kind, Refs: refs}
	}
}

type ResourceLoadedMsg struct {
	Kind     ResKind
	Resource Resource
}

type ErrMsg error

// Command to load a single resource via the loader registered to the given ResKind
func LoadCmd(ref ResourceRef) tea.Cmd {
	log.Debugf("[CMD] Starting Load for %s", ref.Name)
	return func() tea.Msg {
		loader, ok := loaders[ref.Kind]
		if !ok {
			return ErrMsg(fmt.Errorf("no loader for kind %q", ref.Kind))
		}
		res, err := loader(ref.URL)
		if err != nil {
			return ErrMsg(err)
		}
		return ResourceLoadedMsg{Kind: ref.Kind, Resource: res}
	}
}
