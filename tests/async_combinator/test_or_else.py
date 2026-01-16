# AI GENERATED CONTENT
import pytest
from typing import TypeGuard
from async_combinator import AsyncCombinator


class TestAsyncCombinatorOrElse:
    """Test cases for AsyncCombinator.or_else method."""

    @pytest.mark.asyncio
    async def test_or_else_with_matching_exception(self):
        """Test or_else with a matching exception type."""

        async def err_coro() -> int:
            raise ValueError("error")

        async def recover_coro(error: ValueError) -> int:
            return len(str(error))

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        combinator = AsyncCombinator(err_coro())
        result = await combinator.or_else(recover_coro, is_value_error)

        assert result == 5  # len("error") = 5

    @pytest.mark.asyncio
    async def test_or_else_with_successful_completion(self):
        """Test or_else with successful completion - should not call the function."""

        async def ok_coro():
            return 42

        async def never_called_coro(error: ValueError):
            raise AssertionError("This coroutine should never be called")

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        combinator = AsyncCombinator(ok_coro())
        result = await combinator.or_else(never_called_coro, is_value_error)

        assert result == 42

    @pytest.mark.asyncio
    async def test_or_else_chaining(self):
        """Test chaining multiple or_else calls."""

        async def start_coro() -> int:
            raise ValueError("first error")

        async def first_recovery_coro(error: ValueError) -> int:
            raise KeyError("second error")

        async def second_recovery_coro(error: KeyError) -> int:
            return len(error.args[0])

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        def is_key_error(e: BaseException) -> TypeGuard[KeyError]:
            return isinstance(e, KeyError)

        result = await (
            AsyncCombinator(start_coro())
            .or_else(first_recovery_coro, is_value_error)
            .or_else(second_recovery_coro, is_key_error)
        )

        assert result == 12  # len("second error") = 12

    @pytest.mark.asyncio
    async def test_or_else_with_error_in_function(self):
        """Test or_else when the recovery function raises an exception."""

        async def err_coro():
            raise ValueError("original error")

        async def error_coro(error: ValueError):
            raise RuntimeError(f"recovery failed: {error}")

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        combinator = AsyncCombinator(err_coro())

        with pytest.raises(RuntimeError, match="recovery failed: original error"):
            await combinator.or_else(error_coro, is_value_error)

    @pytest.mark.asyncio
    async def test_or_else_with_non_matching_exception(self):
        """Test or_else when the exception doesn't match the guard."""

        async def err_coro():
            raise KeyError("wrong error type")

        async def never_called_coro(error: ValueError):
            raise AssertionError("This coroutine should never be called")

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        combinator = AsyncCombinator(err_coro())

        with pytest.raises(KeyError, match="wrong error type"):
            await combinator.or_else(never_called_coro, is_value_error)

    @pytest.mark.asyncio
    async def test_or_else_with_custom_exception(self):
        """Test or_else with a custom exception type."""

        class CustomError(Exception):
            pass

        async def err_coro() -> str:
            raise CustomError("custom error")

        async def recover_coro(error: CustomError) -> str:
            return f"recovered: {error.args[0]}"

        def is_custom_error(e: BaseException) -> TypeGuard[CustomError]:
            return isinstance(e, CustomError)

        combinator = AsyncCombinator(err_coro())
        result = await combinator.or_else(recover_coro, is_custom_error)

        assert result == "recovered: custom error"

    @pytest.mark.asyncio
    async def test_or_else_with_type_guard(self):
        """Test or_else with a proper TypeGuard."""

        from typing import TypeGuard

        async def err_coro():
            raise ValueError("test error")

        async def recover_coro(error: ValueError):
            return error.args[0].upper()

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        combinator = AsyncCombinator(err_coro())
        result = await combinator.or_else(recover_coro, is_value_error)

        assert result == "TEST ERROR"
