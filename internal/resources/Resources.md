# Resources

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

## Machines

The "Machine" endpoint is unique per version_group. For example, machine/2 is
- Item: TM01 (item/305)
- Move: Mega Punch (move/5)
- VersionGroup: Red-Blue (version/1)

and machine/3 is
- Item: TM01 (item/305)
- Move: Mega Punch (move/5)
- VersionGroup: Yellow (version/2)

These are probably good to store as their own Resource, but don't make them queryable. The item representation of it will suffice, but maybe display them differently?
