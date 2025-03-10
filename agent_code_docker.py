import os
import asyncio
from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.ui import Console
# from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor

async def main():
    # local_code_executor = LocalCommandLineCodeExecutor(work_dir="coding")
    docker_code_executor = DockerCommandLineCodeExecutor(work_dir="coding")
    await docker_code_executor.start()

    code_executor_agent = CodeExecutorAgent(
        name="code_executor",
        code_executor=docker_code_executor,
    )

    stream = code_executor_agent.run_stream(task="""
```python
print("Hello world!!")                                            
```
""")
    
    await Console(stream)
    await docker_code_executor.stop()


asyncio.run(main())

