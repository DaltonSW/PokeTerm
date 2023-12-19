import Utils

ID_TO_NAME_CACHE = {}
NAME_TO_DATA_CACHE = {}
ENDPOINT = 'ability'

class Ability:
    def __init__(self, data):
        global ID_TO_NAME_CACHE
        self.ID = data.get('id')
        self.name = data.get('name')
        self.fromMainSeries = data.get('is_main_series')
        self.firstGeneration = data.get('generation')

        ID_TO_NAME_CACHE[self.ID] = self.name

    def __str__(self):
        return ''


def LoadCache():
    global ID_TO_NAME_CACHE, NAME_TO_DATA_CACHE
    data = Utils.LoadCache(ENDPOINT)
    try:
        ID_TO_NAME_CACHE, NAME_TO_DATA_CACHE = data
    except TypeError:
        print(f"Failed to load {ENDPOINT.upper()} cache")
        pass


def SaveCache():
    global ID_TO_NAME_CACHE, NAME_TO_DATA_CACHE
    if len(NAME_TO_DATA_CACHE) == 0:
        return
    output = (ID_TO_NAME_CACHE, NAME_TO_DATA_CACHE)
    Utils.SaveCache(ENDPOINT, output)


def HandleSearch() -> Ability | None:
    global ID_TO_NAME_CACHE, NAME_TO_DATA_CACHE
    query = input(f'{ENDPOINT.title()} Name or ID: ').lower()

    if query.isdigit():
        query = Utils.ProperQueryFromID(int(query), ID_TO_NAME_CACHE)

    if query in NAME_TO_DATA_CACHE:
        return NAME_TO_DATA_CACHE[query]

    data = Utils.GetFromAPI(ENDPOINT, query)
    if data is not None:
        newObject = Ability(data)
        NAME_TO_DATA_CACHE[newObject.name] = newObject
        return newObject
