```
from tinystore.models import TinyStore

TinyStore.get('omg')  # {'test': 42}
TinyStore.exists('omg')  # False
TinyStore.keys()  # []

TinyStore.set('omg', {'a': 1})

TinyStore.get('omg')  # {'a': 1}
TinyStore.exists('omg')  # True
TinyStore.keys()  # ['omg']

TinyStore.remove_single('omg)
TinyStore.keys()  # []
```

Set defaults in `settings.py`, e.g.

```
TINY_STORE = {
    'omg: {'test': 42},
    'lol: {'key': 'value'},
}
```
