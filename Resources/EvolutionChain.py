from console import console

def PrintEvoChain(chain, charsPrinted=0):
    species = chain["species"]["name"]
    console.print(species.title(), style='bold')
    charsPrinted += len(species.title())

    # Handle the case where there are no further evolutions
    if not chain["evolves_to"]:
        return

    # Process each evolution
    for evolution in chain["evolves_to"]:
        # Extract evolution details
        methodStrLen = 0
        for detail in evolution["evolution_details"]:
            if detail["trigger"]["name"] == "level-up" and detail.get("min_level") is not None:
                method = f"Level {detail['min_level']}"
                methodStrLen = 6 + len(str(detail["min_level"]))
            elif detail["trigger"]["name"] == "use-item" and detail.get("item") is not None:
                method = f"Use {detail['item']['name']}"
                methodStrLen = 4 + len(str(detail["item"]["name"]))
            elif detail["trigger"]["name"] == "trade" and detail.get("held_item") is not None:
                method = f"Trade holding {detail['held_item']['name']}"
                methodStrLen = 14 + len(str(detail["held_item"]["name"]))
            else:
                method = detail["trigger"]["name"]
                methodStrLen = len(str(detail["trigger"]["name"]))
            print(' ' * charsPrinted + f"|- {method} -> ", end="" if len(evolution["evolution_details"]) == 1 else '\n')

        PrintEvoChain(evolution, charsPrinted * 2 + methodStrLen - 1)


class EvolutionChain:
    def __init__(self, data):
        self.ID = data.get('id')

        self.evoChain = data.get('chain')
        self.babyTriggerItem = data.get('baby_trigger_item')

    def PrintData(self):
        PrintEvoChain(self.evoChain)
        pass
