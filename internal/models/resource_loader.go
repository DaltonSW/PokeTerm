package models

import (
	"errors"
	"fmt"
	"io"
	"net/http"
	"strings"

	"github.com/charmbracelet/bubbles/v2/progress"
	"github.com/charmbracelet/bubbles/v2/spinner"
	tea "github.com/charmbracelet/bubbletea/v2"
	"go.dalton.dog/poketerm/internal/resources"
)

type ResourceLoaderModel struct {
	spinner  spinner.Model
	progress progress.Model

	url      string
	endpoint string

	results  []resultItem
	initLoad bool
	count    int
	finished int

	err error
}

func NewResourceLoader(endpoint, url string) (m ResourceLoaderModel) {
	m.url = fmt.Sprintf(url, endpoint)
	m.endpoint = endpoint

	m.progress = progress.New(progress.WithDefaultGradient())
	m.spinner = spinner.New(spinner.WithSpinner(spinner.Ellipsis))
	m.initLoad = true

	return
}

func (m ResourceLoaderModel) Init() tea.Cmd {
	return tea.Batch(m.spinner.Tick, startProcessingURL(m.url))
}

func (m ResourceLoaderModel) Update(msg tea.Msg) (ResourceLoaderModel, tea.Cmd) {
	var cmd tea.Cmd
	var cmds []tea.Cmd

	switch msg := msg.(type) {

	case initLoadMsg:
		if msg.Count < 1 {
			return m, nil
		}

		if !strings.Contains(msg.Results[0].URL, m.endpoint) {
			return m, nil
		}

		m.results = msg.Results
		m.count = msg.Count
		m.initLoad = false

		// Spawn commands for each element
		for _, res := range m.results {
			cmds = append(cmds, processResult(res))
		}
		return m, tea.Batch(cmds...)

	case itemLoadedMsg:

		if !strings.Contains(msg.url, m.endpoint) {
			return m, nil
		}
		m.finished++
		return m, m.progress.SetPercent(float64(m.finished) / float64(m.count))

	case progress.FrameMsg:
		m.progress, cmd = m.progress.Update(msg)
		return m, cmd

	case errMsg:
		m.err = msg

	case tea.KeyMsg:
		if msg.String() == "q" || msg.String() == "ctrl+c" {
			return m, tea.Quit
		}
	case spinner.TickMsg:
		m.spinner, cmd = m.spinner.Update(msg)
		cmds = append(cmds, cmd)
	}

	return m, tea.Batch(cmds...)
}

func (m ResourceLoaderModel) View() string {
	if m.err != nil {
		return fmt.Sprintf("Error occurred: %v", m.err)
	}
	if m.initLoad {
		return "Making first query..."
	}
	s := fmt.Sprintf("Progress: %d/%d\n", m.finished, m.count)
	s += m.progress.View() + "\n"

	if m.finished == m.count {
		s += "\nAll data fetched:\n"
		for _, results := range m.results {
			s += fmt.Sprintf("- %s: %s\n", results.Name, results.URL)
		}
		s += "\nPress q to quit.\n"
	}

	return s
}

// ~~ Messages / Commands ~~

type (
	initialResponse struct {
		Count   int
		Results []resultItem
	}

	resultItem struct {
		Name string
		URL  string
	}
)

type initLoadMsg initialResponse

type itemLoadedMsg struct {
	name string
	url  string
	data []byte
}

type errMsg error

func startProcessingURL(url string) tea.Cmd {
	return func() tea.Msg {
		var data initialResponse
		if err := resources.QueryAndUnmarshal(url, &data); err != nil {
			return errMsg(err)
		}

		return initLoadMsg(data)
	}
}

func processResult(result resultItem) tea.Cmd {
	return func() tea.Msg {
		resp, err := http.Get(result.URL)

		if err != nil {
			return errMsg(err)
		}

		defer resp.Body.Close()

		if resp.StatusCode != 200 {
			return errMsg(errors.New("Request to url " + result.URL + " resulted in a non-200 response"))
		}

		body, err := io.ReadAll(resp.Body)
		if err != nil {
			return errMsg(err)
		}

		return itemLoadedMsg{name: result.Name, data: body, url: result.URL}
	}
}
