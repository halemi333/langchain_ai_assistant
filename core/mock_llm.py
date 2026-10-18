
class MockResponse:
    """Represents a simple mock model response."""

    def __init__(self, content: str):
        self.content = content


class MockLLM:
    """A simple model substitute for local development."""

    def invoke(self, message: str) -> MockResponse:
        return MockResponse(
            content=(
                "[MOCK RESPONSE] "
                f"Received your message: {message}"
            )
        )
