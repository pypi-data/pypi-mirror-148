# UFO Configs

*UFO stands for Urban Flow Observatory. Calm down, conspiracy theorists!*

This code defines a bespoke **configurations manager class**, along with some
useful helper functions.

## Usage

The package which this code defines is intended for use within another Python
project. Usage consists of three parts:

1. Defining a dictionary of **default** configurations.
2. Creating a JSON file of **override** configurations (optional).
3. Creating an immutable **configurations object** using the above.

### Example

First, we define a `DEFAULTS` dictionary:

```python
DEFAULTS = {
    "general": {
        "richard": "red",
        "of": "orange",
        "york": "yellow",
        "gave": "green",
        "battle": "blue",
        "in": "indigo",
        "vain": "violet"
    },
    "other": {
        "tinker": "tailor",
        "soldier": "sailor",
        "rich_man": "poor man",
        "beggar_man": "thief"
    },
    "paths": {
        "path_to_home": "/home/jeff",
        "path_to_somewhere": "/home/jeff/somewhere",
        "path_to_somewhere_else": "/somewhere/else/entirely"
    }
}
```

Then, *if and only if we wish to reset any values*, we create a JSON file at
/path/to/overrides - or wherever we would like to put it.

```json
{
    "general": {
        "of": "ochre",
        "york": null
    },
    "other": {
        "rich_man": "old man"
    },
    "paths": {
        "path_to_home": "/home/jefe"
    }
}
```

Finally, we then create our configs object using the appropriate function:

```python
from ufo_configs import get_configs_object

configs_object = \
    get_configs_object(DEFAULTS, path_to_overrides="/path/to/overrides")
```

If we were then to call the fields of our `configs_object`, we would get the
following responses:

| Call                             | Result      |
| -------------------------------- | ----------- |
| `configs_object.general.richard` | `"red"`     |
| `configs_object.general.of`      | `"ochre"`   |
| `configs_object.general.york`    | `"yellow"`  |
| `configs_object.other.rich_man`  | `"old man"` |


#### Paths

The `paths` field is special in that, if we override, say, path /home/jeff, then
every path which has /home/jeff as its parent will also be updated to reflect
that change.

Thus, in our example, when /home/jeff is overridden to /home/jefe, then
`configs_object.paths.path_to_somewhere` is updated to /home/jeff/somewhere,
whereas `configs_object.paths.path_to_somewhere_else` stays as it was.
