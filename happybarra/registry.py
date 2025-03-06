from functools import partial


def registry(registry_type):
    registry: dict = {}

    def decorated(*args):
        return registry.get(registry_type.__name__)(*args)

    def register(name: str = None):
        def inner(callable_):
            class_name = name or callable_.__name__
            parametrized_callable_ = partial(callable_, class_name)
            registry[class_name] = parametrized_callable_
            print("New process type registered: {class_name}")
            return parametrized_callable_

        return inner

    decorated.register = register
    decorated.registry = registry
    return decorated
