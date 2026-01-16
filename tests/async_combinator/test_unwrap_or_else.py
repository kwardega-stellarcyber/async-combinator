# AI GENERATED CONTENT
import pytest
from typing import TypeGuard
from async_combinator import AsyncCombinator


class TestAsyncCombinatorUnwrapOrElse:
    """Test cases for AsyncCombinator.unwrap_or_else method."""

    @pytest.mark.asyncio
    async def test_unwrap_or_else_with_successful_completion(self):
        """Test unwrap_or_else with successful completion."""

        async def ok_coro() -> int:
            return 42

        def error_func(error: ValueError) -> int:
            raise AssertionError("This function should never be called")

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        combinator = AsyncCombinator(ok_coro())
        result = await combinator.unwrap_or_else(error_func, is_value_error)

        assert result == 42  # Should return the original value

    @pytest.mark.asyncio
    async def test_unwrap_or_else_with_matching_exception(self):
        """Test unwrap_or_else with a matching exception type."""

        async def err_coro() -> int:
            raise ValueError("error")

        def error_func(error: ValueError) -> int:
            return len(error.args[0])

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        combinator = AsyncCombinator(err_coro())
        result = await combinator.unwrap_or_else(error_func, is_value_error)

        assert result == 5  # Should call error_func("error")

    @pytest.mark.asyncio
    async def test_unwrap_or_else_chaining(self):
        """Test chaining multiple unwrap_or_else calls."""

        async def start_coro() -> int:
            raise ValueError("first error")

        def first_error_func(error: ValueError) -> int:
            return len(error.args[0])

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        result = await AsyncCombinator(start_coro()).unwrap_or_else(
            first_error_func, is_value_error
        )

        assert result == 11  # Should call first_error_func("first error")

    @pytest.mark.asyncio
    async def test_unwrap_or_else_with_different_types(self):
        """Test unwrap_or_else with different input and output types."""

        async def err_coro() -> str:
            raise ValueError("error")

        def error_func(error: ValueError) -> str:
            return error.args[0].upper()

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        result = await AsyncCombinator(err_coro()).unwrap_or_else(
            error_func, is_value_error
        )

        assert result == "ERROR"  # Should call error_func("error")

    @pytest.mark.asyncio
    async def test_unwrap_or_else_with_exception_in_error_func(self):
        """Test unwrap_or_else when the error function raises an exception."""

        async def err_coro() -> int:
            raise ValueError("error")

        def exception_func(error: ValueError) -> int:
            raise RuntimeError(f"exception with error: {error}")

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        combinator = AsyncCombinator(err_coro())

        with pytest.raises(RuntimeError, match="exception with error: error"):
            await combinator.unwrap_or_else(exception_func, is_value_error)

    @pytest.mark.asyncio
    async def test_unwrap_or_else_with_complex_objects(self):
        """Test unwrap_or_else with complex objects."""

        async def err_coro() -> dict[str, str | int]:
            raise ValueError("user not found")

        def error_func(error: ValueError) -> dict[str, str | int]:
            return {"id": 0, "name": "default", "error": error.args[0]}

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        result = await AsyncCombinator(err_coro()).unwrap_or_else(
            error_func, is_value_error
        )

        expected = {"id": 0, "name": "default", "error": "user not found"}
        assert result == expected

    @pytest.mark.asyncio
    async def test_unwrap_or_else_with_non_matching_exception(self):
        """Test unwrap_or_else when the exception doesn't match the guard."""

        async def err_coro() -> int:
            raise KeyError("wrong error type")

        def never_called_func(error: ValueError) -> int:
            raise AssertionError("This function should never be called")

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        combinator = AsyncCombinator(err_coro())

        with pytest.raises(KeyError, match="wrong error type"):
            await combinator.unwrap_or_else(never_called_func, is_value_error)

    @pytest.mark.asyncio
    async def test_unwrap_or_else_with_custom_exception(self):
        """Test unwrap_or_else with a custom exception type."""

        class CustomError(Exception):
            pass

        async def err_coro() -> str:
            raise CustomError("custom error")

        def error_func(error: CustomError) -> str:
            return f"recovered: {error.args[0]}"

        def is_custom_error(e: BaseException) -> TypeGuard[CustomError]:
            return isinstance(e, CustomError)

        combinator = AsyncCombinator(err_coro())
        result = await combinator.unwrap_or_else(error_func, is_custom_error)

        assert result == "recovered: custom error"

    @pytest.mark.asyncio
    async def test_unwrap_or_else_vs_or_else_sync_vs_async(self):
        """Test that unwrap_or_else uses synchronous functions vs or_else async."""

        async def err_coro() -> str:
            raise ValueError("error")

        # unwrap_or_else: synchronous fallback
        def sync_fallback(error: ValueError) -> str:
            return f"sync: {error.args[0]}"

        # or_else: async fallback
        async def async_fallback(error: ValueError) -> str:
            return f"async: {error.args[0]}"

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        # Both should work, but unwrap_or_else is simpler for sync values
        unwrap_result = await AsyncCombinator(err_coro()).unwrap_or_else(
            sync_fallback, is_value_error
        )
        or_result = await AsyncCombinator(err_coro()).or_else(
            async_fallback, is_value_error
        )

        assert unwrap_result == "sync: error"
        assert or_result == "async: error"

    @pytest.mark.asyncio
    async def test_unwrap_or_else_with_none_result(self):
        """Test unwrap_or_else when the fallback returns None."""

        async def err_coro() -> None:
            raise ValueError("error")

        def none_func(error: ValueError) -> None:
            return None

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        result = await AsyncCombinator(err_coro()).unwrap_or_else(
            none_func, is_value_error
        )

        assert result is None
