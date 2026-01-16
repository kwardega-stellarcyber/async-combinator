# Async Combinator

A Python library providing functional programming combinators for async operations, inspired by Rust's functional programming patterns and adapted for Python's exception model.

## Features

- **Async Combinators**: Chain async operations with functional combinators (`map`, `then`, `or_else`, etc.)
- **Type-Safe Exception Handling**: Use `TypeGuard` functions to handle specific exception types
- **Composable**: Build complex async workflows from simple operations
- **Type Safety**: Full type hints and generic support with Python 3.12+ type system
- **Exception-Based**: Works with Python's native exception model for error handling

## Installation

```bash
pip install async-combinator
```

Or with Poetry:

```bash
poetry add async-combinator
```

## Quick Start

```python
from async_combinator import AsyncCombinator
from typing import TypeGuard

async def fetch_data():
    return {"id": 1, "name": "Alice"}

def is_value_error(e: BaseException) -> TypeGuard[ValueError]:
    return isinstance(e, ValueError)

# Transform successful results
result = await AsyncCombinator(fetch_data()).map(lambda x: x["name"])
# result == "Alice"

# Chain async operations
async def process_name(name: str):
    return f"Hello, {name}!"

result = await AsyncCombinator(fetch_data()).map(lambda x: x["name"]).then(process_name)
# result == "Hello, Alice!"

# Handle specific exceptions
async def fetch_data_might_fail():
    raise ValueError("Failed to fetch")

async def recover(error: ValueError):
    return {"id": 0, "name": "default_value"}

combinator = AsyncCombinator(fetch_data_might_fail())
result = await combinator.or_else(recover, is_value_error)
# result == {"id": 0, "name": "default_value"}
```

## API Overview

- **`map(f)`**: Transform successful results synchronously
- **`then(f)`**: Chain async operations
- **`or_else(f, error_guard)`**: Recover from specific exceptions with async operations
- **`map_err(f, error_guard)`**: Transform specific exception types
- **`map_ok_or_else(f, e, error_guard)`**: Transform both success and error cases
- **`unwrap_or_else(f, error_guard)`**: Provide synchronous fallback for specific exceptions

All methods preserve exceptions that don't match the `error_guard`, allowing for precise exception handling.