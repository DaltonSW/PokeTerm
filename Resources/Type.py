import Utils

ID_TO_NAME_CACHE = {}
NAME_TO_DATA_CACHE = {}
ENDPOINT = 'type'

class Type:
    def __init__(self, data):
        global ID_TO_NAME_CACHE
        self.ID = data.get('id')
        self.name = data.get('name')

        damageRelations = data.get('damage_relations')
        self.noDamageTo = damageRelations.get('no_damage_to')
        self.halfDamageTo = damageRelations.get('half_damage_to')
        self.doubleDamageTo = damageRelations.get('double_damage_to')
        self.noDamageFrom = damageRelations.get('no_damage_from')
        self.halfDamageFrom = damageRelations.get('half_damage_from')
        self.doubleDamageFrom = damageRelations.get('double_damage_from')

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


def HandleSearch() -> Type | None:
    global ID_TO_NAME_CACHE, NAME_TO_DATA_CACHE
    query = input(f'{ENDPOINT.title()} Name or ID: ').lower()

    if query.isdigit():
        query = Utils.ProperQueryFromID(int(query), ID_TO_NAME_CACHE)

    if query in NAME_TO_DATA_CACHE:
        return NAME_TO_DATA_CACHE[query]

    data = Utils.GetFromAPI(ENDPOINT, query)
    if data is not None:
        newObject = Type(data)
        NAME_TO_DATA_CACHE[newObject.name] = newObject
        return newObject
