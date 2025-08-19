package api

import (
	"encoding/json"
	"errors"
	"io"
	"net/http"

	"github.com/charmbracelet/log"
)

// RespPointer represents a generic Name/URL combo
type RespPointer struct {
	Name string `json:"name"`
	URL  string `json:"url"`
}

// QueryAndUnmarshal will take in any JSON-tagged struct as a generic, and
// attempt to query to given URL and unmarshal it into an instance of the generic
func QueryAndUnmarshal[T any](url string) (T, error) {
	var dest T

	log.Debugf("[API] Querying %s", url)

	resp, err := http.Get(url)

	if err != nil {
		return dest, err
	}

	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return dest, errors.New("Request to url " + url + " resulted in a non-200 response")
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return dest, err
	}

	if err := json.Unmarshal(body, &dest); err != nil {
		return dest, err
	}

	return dest, nil
}
