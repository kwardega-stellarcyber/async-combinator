import pytest
from async_combinator import AsyncCombinator


class TestAsyncCombinatorMap:
    """Test cases for AsyncCombinator.map method."""

    @pytest.mark.asyncio
    async def test_map_basic_functionality(self):
        """Test basic map method functionality."""

        async def initial_coro():
            return 5

        def double_func(value: int) -> int:
            return value * 2

        combinator = AsyncCombinator(initial_coro())
        result = await combinator.map(double_func)

        assert result == 10

    @pytest.mark.asyncio
    async def test_map_with_different_types(self):
        """Test map method with different input and output types."""

        async def string_coro():
            return "hello"

        def length_func(s: str) -> int:
            return len(s)

        def is_even_func(n: int) -> bool:
            return n % 2 == 0

        combinator = AsyncCombinator(string_coro())
        result = await combinator.map(length_func).map(is_even_func)

        assert result is False  # len("hello") = 5, which is odd

    @pytest.mark.asyncio
    async def test_map_chaining(self):
        """Test chaining multiple map calls."""

        async def start_coro():
            return 1

        def add_one_func(n: int) -> int:
            return n + 1

        def multiply_by_two_func(n: int) -> int:
            return n * 2

        def square_func(n: int) -> int:
            return n**2

        result = await (
            AsyncCombinator(start_coro())
            .map(add_one_func)
            .map(multiply_by_two_func)
            .map(square_func)
        )

        # 1 -> 2 -> 4 -> 16
        assert result == 16

    @pytest.mark.asyncio
    async def test_map_with_complex_objects(self):
        """Test map method with complex objects."""

        async def user_coro():
            return {"id": 1, "name": "Alice", "age": 30}

        def extract_name_func(user: dict) -> str:
            return user["name"]

        def greet_func(name: str) -> str:
            return f"Hello, {name}!"

        result = (
            await AsyncCombinator(user_coro()).map(extract_name_func).map(greet_func)
        )

        assert result == "Hello, Alice!"

    @pytest.mark.asyncio
    async def test_map_exception_propagation(self):
        """Test that exceptions in map functions are properly propagated."""

        async def initial_coro():
            return 10

        def failing_func(value: int) -> int:
            raise ValueError(f"Failed with value {value}")

        combinator = AsyncCombinator(initial_coro())

        with pytest.raises(ValueError, match="Failed with value 10"):
            await combinator.map(failing_func)

    @pytest.mark.asyncio
    async def test_map_with_none_values(self):
        """Test map method with None values."""

        async def none_coro():
            return None

        def check_none_func(value) -> bool:
            return value is None

        result = await AsyncCombinator(none_coro()).map(check_none_func)

        assert result is True

    @pytest.mark.asyncio
    async def test_map_with_boolean_logic(self):
        """Test map method with boolean operations."""

        async def number_coro():
            return 7

        def is_prime_func(n: int) -> bool:
            if n < 2:
                return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return False
            return True

        def negate_func(is_prime: bool) -> bool:
            return not is_prime

        result = await (
            AsyncCombinator(number_coro()).map(is_prime_func).map(negate_func)
        )

        assert result is False  # 7 is prime, so not prime = False

    @pytest.mark.asyncio
    async def test_map_return_type_annotation(self):
        """Test that map method properly handles type annotations."""

        async def int_coro() -> int:
            return 42

        def str_func(n: int) -> str:
            return str(n)

        def list_func(s: str) -> list:
            return list(s)

        result = await AsyncCombinator(int_coro()).map(str_func).map(list_func)

        assert result == ["4", "2"]

    @pytest.mark.asyncio
    async def test_map_with_error_in_initial_coro(self):
        """Test that errors in the initial coroutine are propagated through map."""

        async def failing_initial_coro():
            raise RuntimeError("Initial failure")

        def never_called_func(value):
            return value + 1  # This should never be called

        combinator = AsyncCombinator(failing_initial_coro())

        with pytest.raises(RuntimeError, match="Initial failure"):
            await combinator.map(never_called_func)
