package utils

import (
	"strings"

	"golang.org/x/text/cases"
	"golang.org/x/text/language"
)

func StripAndTitle(input string) string {
	output := input
	if strings.Contains(output, "-") {
		output = strings.ReplaceAll(output, "--", "-")
		output = strings.ReplaceAll(output, "-", " ")
	}

	return cases.Title(language.Und).String(output)
}

func Ternary[T any](condition bool, ifTrue, ifFalse T) T {
	if condition {
		return ifTrue
	}
	return ifFalse
}
