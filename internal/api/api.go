package api

import (
	"encoding/json"
	"errors"
	"io"
	"net/http"
)

func QueryAndUnmarshal[T any](url string) (T, error) {
	var dest T

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
