package styles

import "github.com/charmbracelet/lipgloss/v2"

type ListStyles struct {
	Item  lipgloss.Style
	Desc  lipgloss.Style
	Curr  lipgloss.Style
	Match lipgloss.Style
}

func GetListStyles() ListStyles {
	return ListStyles{
		Item:  lipgloss.NewStyle().Foreground(ForeColor),
		Desc:  lipgloss.NewStyle().Foreground(DescColor).Italic(true).Width(8).Align(lipgloss.Right),
		Curr:  lipgloss.NewStyle().Foreground(CurrColor),
		Match: lipgloss.NewStyle().Underline(true).Bold(true),
	}
}
