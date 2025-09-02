"""Tests for the greeting agent."""

import pytest
from unittest.mock import patch, MagicMock
from langchain_core.messages import HumanMessage
from src.hello_phoenix.agent import create_greeting_agent


class TestGreetingAgent:
    """Test suite for greeting agent."""

    @pytest.fixture
    def mock_api_key(self):
        """Mock OpenAI API key."""
        return "test-api-key"

    def test_agent_creation(self, mock_api_key):
        """Test agent can be created."""
        agent = create_greeting_agent(mock_api_key)
        assert agent is not None

    @patch("src.hello_phoenix.agent.ChatOpenAI")
    def test_agent_uses_tools(self, mock_llm, mock_api_key):
        """Test that agent uses tools for greetings."""
        mock_response = MagicMock()
        mock_response.tool_calls = [{"name": "hello_english", "args": {"name": "Test"}}]

        mock_llm_instance = MagicMock()
        mock_llm_instance.bind_tools.return_value.invoke.return_value = mock_response
        mock_llm.return_value = mock_llm_instance

        agent = create_greeting_agent(mock_api_key)

        state = {"messages": [HumanMessage(content="Say hello to Test in English")]}

        result = agent.invoke(state)
        assert "messages" in result

    def test_agent_state_structure(self):
        """Test AgentState structure."""
        from src.hello_phoenix.agent import AgentState

        state = AgentState(messages=[])
        assert "messages" in state
        assert isinstance(state["messages"], list)
