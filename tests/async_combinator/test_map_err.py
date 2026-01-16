# AI GENERATED CONTENT
import pytest
from typing import TypeGuard, Never
from async_combinator import AsyncCombinator


class TestAsyncCombinatorMapErr:
    """Test cases for AsyncCombinator.map_err method."""

    @pytest.mark.asyncio
    async def test_map_err_with_matching_exception(self):
        """Test map_err with a matching exception type."""

        async def err_coro():
            raise ValueError("error")

        def transform_func(error: ValueError) -> Never:
            raise KeyError(f"transformed: {error}")

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        combinator = AsyncCombinator(err_coro())

        with pytest.raises(KeyError, match="transformed: error"):
            await combinator.map_err(transform_func, is_value_error)

    @pytest.mark.asyncio
    async def test_map_err_with_successful_completion(self):
        """Test map_err with successful completion - should not call the function."""

        async def ok_coro():
            return 42

        def never_called_func(error: ValueError) -> Never:
            raise AssertionError("This function should never be called")

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        combinator = AsyncCombinator(ok_coro())
        result = await combinator.map_err(never_called_func, is_value_error)

        assert result == 42

    @pytest.mark.asyncio
    async def test_map_err_chaining(self):
        """Test chaining multiple map_err calls."""

        async def start_coro():
            raise ValueError("first error")

        def first_transform_func(error: ValueError) -> Never:
            raise KeyError(f"first: {error}")

        def second_transform_func(error: KeyError) -> Never:
            raise RuntimeError(f"second: {error.args[0]}")

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        def is_key_error(e: BaseException) -> TypeGuard[KeyError]:
            return isinstance(e, KeyError)

        with pytest.raises(RuntimeError, match="second: first: first error"):
            await (
                AsyncCombinator(start_coro())
                .map_err(first_transform_func, is_value_error)
                .map_err(second_transform_func, is_key_error)
            )

    @pytest.mark.asyncio
    async def test_map_err_with_different_exception_types(self):
        """Test map_err with different input and output exception types."""

        async def err_coro():
            raise ValueError("error")

        def to_key_error_func(error: ValueError) -> Never:
            raise KeyError(len(error.args[0]))

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        combinator = AsyncCombinator(err_coro())

        with pytest.raises(KeyError) as exc_info:
            await combinator.map_err(to_key_error_func, is_value_error)

        # The KeyError should contain the length of "error" which is 5
        assert exc_info.value.args[0] == 5

    @pytest.mark.asyncio
    async def test_map_err_with_exception_in_function(self):
        """Test map_err when the transform function raises an exception."""

        async def err_coro():
            raise ValueError("error")

        def exception_func(error: ValueError) -> Never:
            raise RuntimeError(f"exception with error: {error}")

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        combinator = AsyncCombinator(err_coro())

        with pytest.raises(RuntimeError, match="exception with error: error"):
            await combinator.map_err(exception_func, is_value_error)

    @pytest.mark.asyncio
    async def test_map_err_with_non_matching_exception(self):
        """Test map_err when the exception doesn't match the guard."""

        async def err_coro():
            raise KeyError("wrong error type")

        def never_called_func(error: ValueError) -> Never:
            raise AssertionError("This function should never be called")

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        combinator = AsyncCombinator(err_coro())

        with pytest.raises(KeyError, match="wrong error type"):
            await combinator.map_err(never_called_func, is_value_error)

    @pytest.mark.asyncio
    async def test_map_err_with_custom_exception(self):
        """Test map_err with a custom exception type."""

        class CustomError(Exception):
            pass

        class TransformedError(Exception):
            pass

        async def err_coro():
            raise CustomError("custom error")

        def transform_func(error: CustomError) -> Never:
            raise TransformedError(f"transformed: {error}")

        def is_custom_error(e: BaseException) -> TypeGuard[CustomError]:
            return isinstance(e, CustomError)

        combinator = AsyncCombinator(err_coro())

        with pytest.raises(TransformedError, match="transformed: custom error"):
            await combinator.map_err(transform_func, is_custom_error)

    @pytest.mark.asyncio
    async def test_map_err_preserves_original_exception_when_guard_fails(self):
        """Test that map_err preserves the original exception when guard fails."""

        async def err_coro():
            raise ValueError("original error")

        def never_called_func(error: KeyError) -> Never:
            raise AssertionError("This function should never be called")

        def is_key_error(e: BaseException) -> TypeGuard[KeyError]:
            return isinstance(e, KeyError)

        combinator = AsyncCombinator(err_coro())

        with pytest.raises(ValueError, match="original error"):
            await combinator.map_err(never_called_func, is_key_error)
