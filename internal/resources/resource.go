package resources

import (
	"fmt"

	tea "github.com/charmbracelet/bubbletea/v2"
)

type Resource interface {
	GetName() string
	GetURL() string
	GetRelated() []ResourceRef
}

type ResourceRef struct {
	Name string
	URL  string
	Kind string
}

type LoaderFunc func(url string) (Resource, error)

var loaders = map[string]LoaderFunc{}

func RegisterLoader(kind string, loader LoaderFunc) {
	loaders[kind] = loader
}

// BubbleTea Messages

type ResourceLoadedMsg struct {
	Kind     string
	Resource Resource
}

type ErrMsg error

func LoadCmd(kind, url string) tea.Cmd {
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
