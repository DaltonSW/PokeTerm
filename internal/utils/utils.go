package utils

import (
	"strings"

	"golang.org/x/text/cases"
	"golang.org/x/text/language"
)

func StripAndTitle(input string) string {
	output := input
	output = strings.ReplaceAll(output, "-", " ")

	// Specific replacements
	output = strings.ReplaceAll(output, "  physical", " (physical)")
	output = strings.ReplaceAll(output, "  special", " (special)")
	output = strings.ReplaceAll(output, "10 000 000", "10,000,000")

	return cases.Title(language.Und).String(output)
}

func Ternary[T any](condition bool, ifTrue, ifFalse T) T {
	if condition {
		return ifTrue
	}
	return ifFalse
}
