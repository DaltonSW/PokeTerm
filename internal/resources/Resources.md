# Resources

- 2nd level headers will be references that are loaded and initially searchable
- 3rd level headers are endpoints that contain supplementary information

## Move

- Name
- Accuracy
- Effect Chance
- PP
- Priority
- Power
- Learned By Pokemon (list of name/URLs)
- Generation (name/URL)
- Meta.Ailment (Name is fine, nothing relevant stored in move-ailment endpoint)
- Meta.Category (Name is fine, nothing relevant stored in move-ailment endpoint)
- Meta.CritRate
- Meta.Drain
- Meta.FlinchChance
- Meta.Healing
- Meta.MaxHits
- Meta.MinHits
- Meta.MaxTurns
- Meta.MinTurns
- Meta.StatChance

## Item

- Name
- Cost
- Fling Power
- Fling Effect
- Attributes
- Categories
- Effect Entries
- Sprites
- Held By Pokemon

*I think this should probably sub-differentiate Machines and Berries, since they're items, but have notable additional stuff, but perhaps doesn't warrant their own references/previews?*

### Machine

- Relevant Item
- Move
- Version Group

The "Machine" endpoint is unique per version_group. For example, machine/2 is
- Item: TM01 (item/305)
- Move: Mega Punch (move/5)
- VersionGroup: Red-Blue (version/1)

and machine/3 is
- Item: TM01 (item/305)
- Move: Mega Punch (move/5)
- VersionGroup: Yellow (version/2)

### Berry

- Growth Time
- Size (mm)
- Flavors

- Max Harvest (Gen 4)
- Soil Dryness (Rate at which this berry dries out the soil it's growing in)

- Firmness (PokeBlocks / Poffins)
- Smoothness (PokeBlocks / Poffins)

- Natural Gift Power
- Natural Gift Type

## Generation

*"A grouping of the Pokemon games that separates them based on the Pokemon they include"*
*"In each generation, a new set of Pokemon, Moves, Abilities, and Types that didn't exist in the previous gen are released"*

- Name
- Main Region

- []New Abilities
- []New Moves
- []New Pokemon Species
- []New Types
- []Version Groups

## Version

- ID
- Name
- Version Group

### Version Group

- ID
- Name
- Generation
- []Move Learn Methods
- []Pokedexes
- []Regions
- []Versions

## Stat

- Affecting Moves
    - Decreasing
    - Increasing
- Affecting Natures
    - Decreasing
    - Increasing

## Region

## Location(s)

## Pokemon

## Pokedex
