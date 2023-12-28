from .Data import AbstractData


class Ability(AbstractData):
    ID_TO_NAME_CACHE = {}
    NAME_TO_DATA_CACHE = {}
    ENDPOINT = 'ability'

    def __init__(self, data):
        super().__init__(data)

        self.fromMainSeries = data.get('is_main_series')
        self.firstGeneration = data.get('generation')
        effects = data.get('effect_entries')
        self.shortEffect = None
        self.flavorText = None
        for effect in effects:
            if effect.get('language').get('name') != 'en':
                continue
            self.shortEffect = effect.get('short_effect')
            break

        flavorTexts = data.get('flavor_text_entries')
        for text in flavorTexts:
            if text.get('language').get('name') != 'en':
                continue
            self.flavorText = text.get('flavor_text')
            break

        self.ID_TO_NAME_CACHE[self.ID] = self.name

    @property
    def PrintDescription(self):
        if self.shortEffect is not None:
            return self.shortEffect
        if self.flavorText is not None:
            return self.flavorText
        return "No description available"

    def PrintData(self):
        return

    def AddToCache(self):
        super().AddToCache()

    # region Formatted Getters
    # @property
    # def FormattedResourceProperty(self) -> str:
    #     return colored(self.property.title(), Colors.GetWhateverColor(self.property))

    # endregion
