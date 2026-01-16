# AI GENERATED CONTENT
import pytest
from typing import TypeGuard, Never
from async_combinator import AsyncCombinator


class TestAsyncCombinatorMapOkOrElse:
    """Test cases for AsyncCombinator.map_ok_or_else method."""

    @pytest.mark.asyncio
    async def test_map_ok_or_else_with_successful_completion(self):
        """Test map_ok_or_else with successful completion."""

        async def ok_coro():
            return 5

        def double_func(value: int) -> int:
            return value * 2

        def error_func(error: ValueError) -> Never:
            raise AssertionError("This function should never be called")

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        combinator = AsyncCombinator(ok_coro())
        result = await combinator.map_ok_or_else(
            double_func, error_func, is_value_error
        )

        assert result == 10  # Should call double_func(5)

    @pytest.mark.asyncio
    async def test_map_ok_or_else_with_matching_exception(self):
        """Test map_ok_or_else with a matching exception type."""

        async def err_coro():
            raise ValueError("error")

        def ok_func(value: int) -> int:
            raise AssertionError("This function should never be called")

        def error_func(error: ValueError) -> Never:
            raise KeyError(len(error.args[0]))

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        combinator = AsyncCombinator(err_coro())

        with pytest.raises(KeyError) as exc_info:
            await combinator.map_ok_or_else(ok_func, error_func, is_value_error)

        # The KeyError should contain the length of "error" which is 5
        assert exc_info.value.args[0] == 5

    @pytest.mark.asyncio
    async def test_map_ok_or_else_chaining(self):
        """Test chaining multiple map_ok_or_else calls."""

        async def start_coro():
            return 1

        def add_one_func(value: int) -> int:
            return value + 1

        def error_func(error: ValueError) -> Never:
            raise KeyError(len(error.args[0]))

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        result = await AsyncCombinator(start_coro()).map_ok_or_else(
            add_one_func, error_func, is_value_error
        )

        assert result == 2  # Should call add_one_func(1)

    @pytest.mark.asyncio
    async def test_map_ok_or_else_with_different_types(self):
        """Test map_ok_or_else with different input and output types."""

        async def ok_coro():
            return "hello"

        def length_func(s: str) -> int:
            return len(s)

        def error_func(error: ValueError) -> Never:
            raise KeyError(len(error.args[0]))

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        result = await AsyncCombinator(ok_coro()).map_ok_or_else(
            length_func, error_func, is_value_error
        )

        assert result == 5  # Should call length_func("hello")

    @pytest.mark.asyncio
    async def test_map_ok_or_else_with_exception_in_ok_func(self):
        """Test map_ok_or_else when the ok function raises an exception."""

        async def ok_coro():
            return 5

        def exception_func(value: int) -> int:
            raise ValueError(f"exception with value {value}")

        def error_func(error: ValueError) -> Never:
            raise KeyError(len(error.args[0]))

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        combinator = AsyncCombinator(ok_coro())

        with pytest.raises(ValueError, match="exception with value 5"):
            await combinator.map_ok_or_else(exception_func, error_func, is_value_error)

    @pytest.mark.asyncio
    async def test_map_ok_or_else_with_exception_in_error_func(self):
        """Test map_ok_or_else when the error function raises an exception."""

        async def err_coro():
            raise ValueError("error")

        def ok_func(value: int) -> int:
            return value * 2

        def exception_func(error: ValueError) -> Never:
            raise KeyError(f"exception with error: {error}")

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        combinator = AsyncCombinator(err_coro())

        with pytest.raises(KeyError, match="exception with error: error"):
            await combinator.map_ok_or_else(ok_func, exception_func, is_value_error)

    @pytest.mark.asyncio
    async def test_map_ok_or_else_with_non_matching_exception(self):
        """Test map_ok_or_else when the exception doesn't match the guard."""

        async def err_coro():
            raise KeyError("wrong error type")

        def ok_func(value: int) -> int:
            raise AssertionError("This function should never be called")

        def error_func(error: ValueError) -> Never:
            raise AssertionError("This function should never be called")

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        combinator = AsyncCombinator(err_coro())

        with pytest.raises(KeyError, match="wrong error type"):
            await combinator.map_ok_or_else(ok_func, error_func, is_value_error)

    @pytest.mark.asyncio
    async def test_map_ok_or_else_with_custom_exception(self):
        """Test map_ok_or_else with a custom exception type."""

        class CustomError(Exception):
            pass

        async def err_coro():
            raise CustomError("custom error")

        def ok_func(value: int) -> int:
            raise AssertionError("This function should never be called")

        def error_func(error: CustomError) -> Never:
            raise ValueError(f"transformed: {error}")

        def is_custom_error(e: BaseException) -> TypeGuard[CustomError]:
            return isinstance(e, CustomError)

        combinator = AsyncCombinator(err_coro())

        with pytest.raises(ValueError, match="transformed: custom error"):
            await combinator.map_ok_or_else(ok_func, error_func, is_custom_error)

    @pytest.mark.asyncio
    async def test_map_ok_or_else_coalesces_to_same_type(self):
        """Test that map_ok_or_else can coalesce success and error to the same type."""

        async def ok_coro():
            return 10

        def success_func(value: int) -> str:
            return f"success: {value}"

        def error_func(error: ValueError) -> Never:
            raise RuntimeError("error occurred")

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        result = await AsyncCombinator(ok_coro()).map_ok_or_else(
            success_func, error_func, is_value_error
        )

        assert result == "success: 10"

    @pytest.mark.asyncio
    async def test_map_ok_or_else_with_none_result(self):
        """Test map_ok_or_else when the success function returns None."""

        async def ok_coro():
            return "test"

        def none_func(value: str) -> None:
            return None

        def error_func(error: ValueError) -> Never:
            raise RuntimeError("error occurred")

        def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
            return isinstance(e, ValueError)

        result = await AsyncCombinator(ok_coro()).map_ok_or_else(
            none_func, error_func, is_value_error
        )

        assert result is None
