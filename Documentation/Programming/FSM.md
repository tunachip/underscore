## Finite State Machine

### Notes on `**kwargs`

Any number of named arguments passed in as a dictionary.

Example:
```python
def enter(self, **kwargs):
    pass
```

is passed by calling it like this:
```python
fsm.change('menu', instanceID="IDxx1", debug_mode=True, stacked_iters=2)
```

internally it would be:

```python
kwargs = {
    'instanceID': 'IDxx1',
    'debug_mode': True,
    'stacked_iters': 2
}
```

So in the `enter()` method one could write:

```python
def enter(self, **kwargs)
    if kwargs.get('debug_mode'):
        print("Debug baby!!")
```

