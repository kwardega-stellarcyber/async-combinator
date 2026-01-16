from typing import Any, Awaitable, Callable, Coroutine, Generator, Never, TypeGuard

from ._error_guard import error_guard

__all__ = ["AsyncCombinator", "error_guard"]


class AsyncCombinator[T]:
    def __init__(self, awaitable: Awaitable[T]):
        self._awaitable = awaitable

    def __await__(self) -> Generator[Any, Any, T]:
        return self._awaitable.__await__()

    async def _coro(self) -> T:
        return await self

    def __call__(self) -> Coroutine[Any, Any, T]:
        return self._coro()

    def map[U](self, f: Callable[[T], U]) -> "AsyncCombinator[U]":
        """
        Map this awaitable's output to a different type, returning a new awaitable of
        the resulting type.

        This function transforms the successful result of the awaitable by applying
        the function f. If the awaitable raises an exception, that exception is
        propagated without calling f.

        This is useful to chain along a computation once an awaitable has been resolved
        successfully.
        """

        async def map_coro():
            return f(await self)

        return AsyncCombinator(map_coro())

    def then[U](self, f: Callable[[T], Awaitable[U]]) -> "AsyncCombinator[U]":
        """
        Chain on a computation for when an awaitable finishes, passing the result of
        the awaitable to the provided function f.

        The function f must return an awaitable (coroutine, Task, or Future) that
        represents additional work to be done before the composed awaitable is
        finished.

        The function f is only called after successful completion of this awaitable.
        If this awaitable raises an exception, f is not called and the exception is
        propagated.
        """

        async def then_coro():
            return await f(await self)

        return AsyncCombinator(then_coro())

    def or_else[SelfErr: BaseException](
        self,
        f: Callable[[SelfErr], Awaitable[T]],
        error_guard: Callable[[BaseException], TypeGuard[SelfErr]],
    ) -> "AsyncCombinator[T]":
        """
        Executes another awaitable if this one raises a specific exception type.

        The error value is passed to the function f to create a recovery awaitable.
        The error_guard function is used to determine if the raised exception matches
        the expected type SelfErr.

        The provided function f will only be called if this awaitable raises an
        exception that passes the error_guard check. If this awaitable completes
        successfully, f is never called. If the exception doesn't match the guard,
        it is re-raised without calling f.

        The return type of the awaitable returned by f must match the return type T
        of this awaitable.
        """

        async def or_else_coro():
            try:
                return await self
            except BaseException as e:
                if error_guard(e):
                    return await f(e)
                raise

        return AsyncCombinator(or_else_coro())

    def map_err[U, SelfErr: BaseException](
        self,
        f: Callable[[SelfErr], Never],
        error_guard: Callable[[BaseException], TypeGuard[SelfErr]],
    ) -> "AsyncCombinator[T]":
        """
        Transforms a specific exception type into a different exception.

        This method can be used to change the exception type raised by this awaitable
        into a different exception type. The error_guard function is used to determine
        if the raised exception matches the expected type SelfErr.

        The provided function f will only be called if this awaitable raises an
        exception that passes the error_guard check. The function f should raise a
        new exception (since it returns Never). If this awaitable completes successfully,
        f is never called. If the exception doesn't match the guard, it is re-raised
        without calling f.

        This is useful for normalizing exception types or converting between different
        exception hierarchies.
        """

        async def map_err_coro():
            try:
                return await self
            except BaseException as e:
                if error_guard(e):
                    # f should raise
                    try:
                        f(e)
                    except BaseException as f_e:
                        raise f_e from None
                raise

        return AsyncCombinator(map_err_coro())

    def map_ok_or_else[U, SelfErr: BaseException](
        self,
        f: Callable[[T], U],
        e: Callable[[SelfErr], Never],
        error_guard: Callable[[BaseException], TypeGuard[SelfErr]],
    ) -> "AsyncCombinator[U]":
        """
        Transforms both successful results and specific exceptions into a common type.

        This method can be used to coalesce successful results and exceptions into
        a single type U. The function f transforms successful results, while the
        function e handles specific exception types (and should raise a new exception
        since it returns Never).

        The provided function f will only be called if this awaitable completes
        successfully. The provided function e will only be called if this awaitable
        raises an exception that passes the error_guard check. If the exception
        doesn't match the guard, it is re-raised without calling e.

        This is useful when you want to handle both success and error cases in a
        unified way, or when you need to transform exceptions into a different form.
        """

        async def map_ok_or_else_coro():
            try:
                result = await self

            except BaseException as _e:
                if error_guard(_e):
                    # e should raise
                    try:
                        e(_e)
                    except BaseException as e_e:
                        raise e_e from None
                raise
            return f(result)

        return AsyncCombinator(map_ok_or_else_coro())

    def unwrap_or_else[SelfErr: BaseException](
        self,
        f: Callable[[SelfErr], T],
        error_guard: Callable[[BaseException], TypeGuard[SelfErr]],
    ) -> "AsyncCombinator[T]":
        """
        Returns the successful value, or computes a default value synchronously
        if a specific exception type is raised.

        Unlike or_else, this method uses a synchronous function to compute the
        default value, avoiding the need to await another coroutine. This is useful
        for simple fallback values that don't require async operations.

        The provided function f will only be called if this awaitable raises an
        exception that passes the error_guard check. If this awaitable completes
        successfully, f is never called and the original value is returned. If the
        exception doesn't match the guard, it is re-raised without calling f.

        The return type of f must match the return type T of this awaitable.

        Example:
            # With or_else (async recovery):
            result = await combinator.or_else(
                lambda e: async_fallback_function(e),
                is_value_error
            )

            # With unwrap_or_else (sync recovery):
            result = await combinator.unwrap_or_else(
                lambda e: "default_value",  # Simple synchronous fallback
                is_value_error
            )
        """

        async def unwrap_or_else_coro():
            try:
                return await self
            except BaseException as e:
                if error_guard(e):
                    return f(e)
                raise

        return AsyncCombinator(unwrap_or_else_coro())
