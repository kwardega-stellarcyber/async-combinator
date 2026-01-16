import pytest
import asyncio
from async_combinator import AsyncCombinator


class TestAsyncCombinatorBasic:
    """Test cases for basic AsyncCombinator functionality."""

    @pytest.mark.asyncio
    async def test_basic_functionality(self):
        """Test basic AsyncCombinator functionality with a simple coroutine."""

        async def simple_coro():
            return "test_result"

        combinator = AsyncCombinator(simple_coro())
        result = await combinator

        assert result == "test_result"

    @pytest.mark.asyncio
    async def test_with_async_function(self):
        """Test AsyncCombinator with an async function that returns different types."""

        async def async_function():
            return 42

        combinator = AsyncCombinator(async_function())
        result = await combinator

        assert result == 42
        assert isinstance(result, int)

    @pytest.mark.asyncio
    async def test_with_complex_return_value(self):
        """Test AsyncCombinator with complex return values."""

        async def complex_coro():
            return {"key": "value", "number": 123, "list": [1, 2, 3]}

        combinator = AsyncCombinator(complex_coro())
        result = await combinator

        assert result == {"key": "value", "number": 123, "list": [1, 2, 3]}
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_with_exception_handling(self):
        """Test AsyncCombinator properly propagates exceptions."""

        async def failing_coro():
            raise ValueError("test error")

        combinator = AsyncCombinator(failing_coro())

        with pytest.raises(ValueError, match="test error"):
            await combinator

    @pytest.mark.asyncio
    async def test_with_asyncio_task(self):
        """Test AsyncCombinator with an asyncio Task."""

        async def task_coro():
            await asyncio.sleep(0.01)  # Small delay to make it async
            return "task_result"

        task = asyncio.create_task(task_coro())
        combinator = AsyncCombinator(task)
        result = await combinator

        assert result == "task_result"

    @pytest.mark.asyncio
    async def test_with_future(self):
        """Test AsyncCombinator with an asyncio Future."""
        future = asyncio.Future()
        future.set_result("future_result")

        combinator = AsyncCombinator(future)
        result = await combinator

        assert result == "future_result"

    @pytest.mark.asyncio
    async def test_multiple_await_calls(self):
        """Test that AsyncCombinator can be awaited multiple times with different awaitables."""
        call_count = 0

        async def counting_coro():
            nonlocal call_count
            call_count += 1
            return f"call_{call_count}"

        # Create separate awaitables for each call
        combinator1 = AsyncCombinator(counting_coro())
        combinator2 = AsyncCombinator(counting_coro())

        # Await multiple times
        result1 = await combinator1
        result2 = await combinator2

        # Should return different results since we're using different awaitables
        assert result1 == "call_1"
        assert result2 == "call_2"
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_none_return_value(self):
        """Test AsyncCombinator with a coroutine that returns None."""

        async def none_coro():
            return None

        combinator = AsyncCombinator(none_coro())
        result = await combinator

        assert result is None

    @pytest.mark.asyncio
    async def test_boolean_return_value(self):
        """Test AsyncCombinator with boolean return values."""

        async def true_coro():
            return True

        async def false_coro():
            return False

        true_combinator = AsyncCombinator(true_coro())
        false_combinator = AsyncCombinator(false_coro())

        assert await true_combinator is True
        assert await false_combinator is False

    @pytest.mark.asyncio
    async def test_initialization_with_non_awaitable(self):
        """Test that AsyncCombinator can be initialized with non-awaitable but fails when awaited."""
        # AsyncCombinator doesn't validate at initialization time
        combinator = AsyncCombinator("not an awaitable")  # type: ignore

        # But it should fail when we try to await it
        with pytest.raises(
            AttributeError, match="'str' object has no attribute '__await__'"
        ):
            await combinator

    @pytest.mark.asyncio
    async def test_await_method_returns_generator(self):
        """Test that the __await__ method returns a generator."""

        async def test_coro():
            return "test"

        combinator = AsyncCombinator(test_coro())
        generator = combinator.__await__()

        assert hasattr(generator, "__iter__")
        assert hasattr(generator, "__next__")

        # Verify it works correctly
        result = await combinator
        assert result == "test"
