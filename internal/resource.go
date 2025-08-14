package internal

import (
	"fmt"

	tea "github.com/charmbracelet/bubbletea/v2"
	"go.dalton.dog/poketerm/internal/api"
)

type ResKind string

const (
	Pokemon ResKind = "pokemon"
	Type    ResKind = "type"
	Ability ResKind = "ability"
	Move    ResKind = "move"
	Berry   ResKind = "berry"
)

type Resource interface {
	GetName() string
	GetURL() string
	GetRelated() []ResourceRef

	// TODO: GetModel() tea.Model
}

type ResourceRef struct {
	Name string
	URL  string
	Kind ResKind
}

func (ref ResourceRef) Title() string       { return ref.Name }
func (ref ResourceRef) Description() string { return string(ref.Kind) }
func (ref ResourceRef) FilterValue() string { return ref.Name }

type LoaderFunc func(url string) (Resource, error)

var loaders = map[ResKind]LoaderFunc{}

func RegisterLoader(kind ResKind, loader LoaderFunc) {
	loaders[kind] = loader
}

// BubbleTea Messages

type getRefsResponse struct {
	Count   int `json:"count"`
	Results []struct {
		Name string `json:"name"`
		URL  string `json:"url"`
	} `json:"results"`
}

type RefsLoadedMsg struct {
	Kind ResKind
	Refs []ResourceRef
}

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

func LoadCmd(kind ResKind, url string) tea.Cmd {
	return func() tea.Msg {
		loader, ok := loaders[kind]
		if !ok {
			return ErrMsg(fmt.Errorf("no loader for kind %q", kind))
		}
		res, err := loader(url)
		if err != nil {
			return ErrMsg(err)
		}
		return ResourceLoadedMsg{Kind: kind, Resource: res}
	}
}
