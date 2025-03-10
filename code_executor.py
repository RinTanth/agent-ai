import os
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo, ModelFamily
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console

async def main():
    model_client_ollama = OpenAIChatCompletionClient(
        model="codegemma",
        base_url=os.environ["OLLAMA_BASE_URL"],
        model_info=ModelInfo(
            vision=False,
            function_calling=True,
            json_output=False,
            family=ModelFamily.UNKNOWN,
        )
    )

    programmer_agent = AssistantAgent(
        name="programmer",
        model_client=model_client_ollama,
        system_message="""
Yor're a senior programmer who writes code.
IMPORTANT: Wait for execute your code and then you can reply with the word "TERMINATE".
DO NOT OUTPUT "TERMINATE" after your code block.
"""
    )

    code_executor_agent = CodeExecutorAgent(
        name="code_executor",
        code_executor=LocalCommandLineCodeExecutor(work_dir="coding"),
    )

    termination = TextMentionTermination(text="TERMINATE")

    team = RoundRobinGroupChat(
        participants=[programmer_agent, code_executor_agent],
        termination_condition=termination,
    )

    # stream = team.run_stream(task="Write a python script to print 'Hello from team agent'.")
    stream = team.run_stream(task="Provide code to count the number of prime numbers from 1 to 10000.")
    await Console(stream)



asyncio.run(main())