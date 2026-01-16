import pytest
import asyncio
from async_combinator import AsyncCombinator


class TestAsyncCombinatorThen:
    """Test cases for AsyncCombinator.then method."""

    @pytest.mark.asyncio
    async def test_then_basic_functionality(self):
        """Test basic then method functionality."""

        async def initial_coro():
            return 5

        async def double_coro(value: int):
            return value * 2

        combinator = AsyncCombinator(initial_coro())
        result = await combinator.then(double_coro)

        assert result == 10

    @pytest.mark.asyncio
    async def test_then_with_different_types(self):
        """Test then method with different input and output types."""

        async def string_coro():
            return "hello"

        async def length_coro(s: str):
            return len(s)

        async def is_even_coro(n: int):
            return n % 2 == 0

        combinator = AsyncCombinator(string_coro())
        result = await combinator.then(length_coro).then(is_even_coro)

        assert result is False  # len("hello") = 5, which is odd

    @pytest.mark.asyncio
    async def test_then_chaining(self):
        """Test chaining multiple then calls."""

        async def start_coro():
            return 1

        async def add_one_coro(n: int):
            return n + 1

        async def multiply_by_two_coro(n: int):
            return n * 2

        async def square_coro(n: int):
            return n**2

        result = await (
            AsyncCombinator(start_coro())
            .then(add_one_coro)
            .then(multiply_by_two_coro)
            .then(square_coro)
        )

        # 1 -> 2 -> 4 -> 16
        assert result == 16

    @pytest.mark.asyncio
    async def test_then_with_complex_objects(self):
        """Test then method with complex objects."""

        async def user_coro():
            return {"id": 1, "name": "Alice", "age": 30}

        async def extract_name_coro(user: dict):
            return user["name"]

        async def greet_coro(name: str):
            return f"Hello, {name}!"

        result = (
            await AsyncCombinator(user_coro()).then(extract_name_coro).then(greet_coro)
        )

        assert result == "Hello, Alice!"

    @pytest.mark.asyncio
    async def test_then_exception_propagation(self):
        """Test that exceptions in then functions are properly propagated."""

        async def initial_coro():
            return 10

        async def failing_coro(value: int):
            raise ValueError(f"Failed with value {value}")

        combinator = AsyncCombinator(initial_coro())

        with pytest.raises(ValueError, match="Failed with value 10"):
            await combinator.then(failing_coro)

    @pytest.mark.asyncio
    async def test_then_with_async_sleep(self):
        """Test then method with async operations that include delays."""

        async def slow_coro():
            await asyncio.sleep(0.01)
            return "slow_result"

        async def process_coro(s: str):
            await asyncio.sleep(0.01)
            return f"processed_{s}"

        start_time = asyncio.get_event_loop().time()
        result = await AsyncCombinator(slow_coro()).then(process_coro)
        end_time = asyncio.get_event_loop().time()

        assert result == "processed_slow_result"
        assert end_time - start_time >= 0.02  # Should take at least 20ms

    @pytest.mark.asyncio
    async def test_then_with_none_values(self):
        """Test then method with None values."""

        async def none_coro():
            return None

        async def check_none_coro(value):
            return value is None

        result = await AsyncCombinator(none_coro()).then(check_none_coro)

        assert result is True

    @pytest.mark.asyncio
    async def test_then_with_boolean_logic(self):
        """Test then method with boolean operations."""

        async def number_coro():
            return 7

        async def is_prime_coro(n: int):
            if n < 2:
                return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return False
            return True

        async def is_odd_coro(n: int):
            return n % 2 == 1

        async def negate_coro(is_prime: bool):
            return not is_prime

        result = await (
            AsyncCombinator(number_coro()).then(is_prime_coro).then(negate_coro)
        )

        assert result is False  # 7 is prime, so not prime = False

    @pytest.mark.asyncio
    async def test_then_return_type_annotation(self):
        """Test that then method properly handles type annotations."""

        async def int_coro() -> int:
            return 42

        async def str_coro(n: int) -> str:
            return str(n)

        async def list_coro(s: str) -> list:
            return list(s)

        result = await AsyncCombinator(int_coro()).then(str_coro).then(list_coro)

        assert result == ["4", "2"]

    @pytest.mark.asyncio
    async def test_then_with_error_in_initial_coro(self):
        """Test that errors in the initial coroutine are propagated through then."""

        async def failing_initial_coro():
            raise RuntimeError("Initial failure")

        async def never_called_coro(value):
            return value + 1  # This should never be called

        combinator = AsyncCombinator(failing_initial_coro())

        with pytest.raises(RuntimeError, match="Initial failure"):
            await combinator.then(never_called_coro)

    @pytest.mark.asyncio
    async def test_then_with_task_and_future(self):
        """Test then method with asyncio Task and Future objects."""

        async def task_coro():
            await asyncio.sleep(0.01)
            return "task_result"

        async def future_coro(s: str):
            future = asyncio.Future()
            future.set_result(f"future_{s}")
            return await future

        task = asyncio.create_task(task_coro())
        result = await AsyncCombinator(task).then(future_coro)

        assert result == "future_task_result"
