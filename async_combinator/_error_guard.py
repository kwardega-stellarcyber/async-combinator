from typing import Callable, TypeGuard


def error_guard[T](
    *classes: type[T],
) -> Callable[[BaseException], TypeGuard[T]]:
    def guard(e: BaseException) -> TypeGuard[T]:
        return isinstance(e, classes)

    return guard
