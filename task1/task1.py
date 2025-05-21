import functools

def strict(func):
    annotations = func.__annotations__
    names = func.__code__.co_varnames

    @functools.wraps(func)
    def wrapper(*args):
        for i in range(len(args)):
            name = names[i]
            value = args[i]
            if name in annotations:
                expected_type = annotations[name]
                if not isinstance(value, expected_type):
                    raise TypeError(f"{name} должен быть {expected_type.__name__}, а не {type(value).__name__}")

        return func(*args)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


@strict
def concat(a: str, b: str) -> str:
    return a + b


@strict
def is_adult(age: int, consent: bool) -> bool:
    return age >= 18 and consent


@strict
def sum_two_float(a: float, b: float) -> float:
    return a + b


tests = [
    {
        'func': sum_two,
        'args': (1, 2),
        'expected': 3,
        'raises': None
    },
    {
        'func': sum_two,
        'args': (1, 2.5),
        'expected': None,
        'raises': TypeError
    },
    {
        'func': concat,
        'args': ("hello", "world"),
        'expected': "helloworld",
        'raises': None
    },
    {
        'func': concat,
        'args': ("hello", 5),
        'expected': None,
        'raises': TypeError
    },
    {
        'func': is_adult,
        'args': (20, True),
        'expected': True,
        'raises': None
    },
    {
        'func': is_adult,
        'args': ("18", True),
        'expected': None,
        'raises': TypeError
    },
    {
        'func': sum_two_float,
        'args': (1.0, 2.0),
        'expected': 3.0,
        'raises': None
    },
    {
        'func': sum_two_float,
        'args': (1, 2.0),
        'expected': None,
        'raises': TypeError
    },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        func = test['func']
        args = test['args']
        expected = test['expected']
        should_raise = test['raises']

        if should_raise:
            try:
                result = func(*args)
                raise AssertionError(f"Тест {i} провален [{func.__name__}{args}]: ожидаемая ошибка - {should_raise.__name__}, полученный результат - {result}")
            except Exception as e:
                assert isinstance(e, should_raise), f"Тест {i} провален [{func.__name__}{args}]: ожидалось - {should_raise.__name__}, полученный результат - {type(e).__name__}"
                print(f"Тест {i} пройден [{func.__name__}{args}] (получен {should_raise.__name__}: {e})")
        else:
            result = func(*args)
            assert result == expected, f"Тест {i} провален [{func.__name__}{args}]: ожидаемый результат - {expected}, полученный результат - {result}"
            print(f"Тест {i} пройден [{func.__name__}{args}] (полученный результат - {result})")
