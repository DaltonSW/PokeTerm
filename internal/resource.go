package internal

import (
	"fmt"

	tea "github.com/charmbracelet/bubbletea/v2"
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

type LoaderFunc func(url string) (Resource, error)

var loaders = map[ResKind]LoaderFunc{}

func RegisterLoader(kind ResKind, loader LoaderFunc) {
	loaders[kind] = loader
}

// BubbleTea Messages

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
