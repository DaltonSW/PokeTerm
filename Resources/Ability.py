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
        for effect in effects:
            if effect.get('language').get('name') != 'en':
                continue
            self.description = effect.get('short_effect')
            break

        self.ID_TO_NAME_CACHE[self.ID] = self.name

    def PrintData(self):
        return

    def AddToCache(self):
        super().AddToCache()

    # region Formatted Getters
    # @property
    # def FormattedResourceProperty(self) -> str:
    #     return colored(self.property.title(), Colors.GetWhateverColor(self.property))

    # endregion
