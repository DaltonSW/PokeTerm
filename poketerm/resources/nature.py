from poketerm.console import console
from poketerm.resources.data import Resource


class Nature(Resource):
    MAX_COUNT = 24
    ENDPOINT = "nature"
    VALID_NAMES = set()

    def __init__(self, data):
        super().__init__(data)

        decreasedStatData = data.get("decreased_stat")
        self.decreasedStat = (
            "N/A" if decreasedStatData is None else decreasedStatData.get("name")
        )
        increasedStatData = data.get("increased_stat")
        self.increasedStat = (
            "N/A" if increasedStatData is None else increasedStatData.get("name")
        )
        hatesFlavorData = data.get("hates_flavor")
        self.hatesFlavor = (
            "N/A" if hatesFlavorData is None else hatesFlavorData.get("name")
        )
        likesFlavorData = data.get("likes_flavor")
        self.likesFlavor = (
            "N/A" if likesFlavorData is None else likesFlavorData.get("name")
        )

        # also has move_battle_style_preferences and pokeathlon_stat_changes

    def print_data(self):
        console.rule(f"[bold]{self.print_name}", align="left", style="none")
        console.print(f"[attack]Increased Stat: [/]{self.increasedStat.title()}")
        console.print(f"[defense]Decreased Stat: [/]{self.decreasedStat.title()}")
        print()
        console.print(f"[attack]Likes Flavor: [/]{self.likesFlavor.title()}")
        console.print(f"[defense]Hates Flavor: [/]{self.hatesFlavor.title()}")

    def __str__(self):
        return ""
