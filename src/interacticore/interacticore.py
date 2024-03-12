# MIT License
#
# Copyright (c) 2024, Justin Randall, Smart Interactive Transformations Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from abc import ABC, abstractmethod
from langchain_core.exceptions import OutputParserException
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.language_models.llms import BaseLLM
from langchain_core.output_parsers.transform import BaseCumulativeTransformOutputParser
from langchain_core.prompts.base import BasePromptTemplate
from langchain_core.tracers.context import tracing_v2_enabled

import random
import time
import logging

from .utils import Utils

# Create a logger with the module name
log = logging.getLogger(__name__)


def retry_with_exponential_backoff(
        func,
        initial_delay: float = 1,
        exponential_base: float = 2,
        jitter: bool = True,
        max_retries: int = 3,
        errors: tuple = (OutputParserException,),
):
    """
    Retry a function with exponential backoff.
    :param func:
    :param initial_delay:
    :param exponential_base:
    :param jitter:
    :param max_retries:
    :param errors:
    :return:
    """
    def wrapper(*args, **kwargs):
        num_retries = 0
        delay = initial_delay
        while True:
            try:
                return func(*args, **kwargs)
            except errors as e:
                log.error(f"Caught exception: {e}")
                num_retries += 1
                if num_retries > max_retries:
                    raise Exception(
                        f"Maximum number of retries ({max_retries}) exceeded."
                    )
                delay *= exponential_base * (1 + jitter * random.random())
                time.sleep(delay)
            except Exception as e:
                raise e
    return wrapper


class LangChainWrapProxy(ABC):
    """
    Define LangChainWrap proxy interface.
    """
    @abstractmethod
    def execute(self, **kwargs):
        """Submit a command for execution."""
        pass


class LangChainCommand(ABC):
    """
    Abstract command object for implementing LangChainWrap commands.
    """
    def __init__(self,
                 *,
                 session_id: str = None,
                 cmd_name: str = None,
                 sys_prompt: str = None,
                 user_prompt_tmpl: str = None,
                 output_parser: BaseCumulativeTransformOutputParser = None,
                 ):
        """
        Construct a new instance.
        :param session_id: The session_id.
        :param cmd_name: The command name.
        :param sys_prompt: The system prompt.  This is not a prompt template.
        :param user_prompt_tmpl: The user prompt template.
        :param output_parser: The specified endpoint output parser.
        """

        if session_id is None:
            session_id = Utils.new_session_id()

        if cmd_name is None:
            raise Exception('cmd_name is required')

        self.session_id: str = session_id
        self.cmd_name: str = cmd_name
        self.exec_time: float | None = None
        self.sys_prompt: str = sys_prompt
        self.user_prompt_tmpl: str = user_prompt_tmpl
        self.output_parser: BaseCumulativeTransformOutputParser = output_parser
        self.result = None

    @abstractmethod
    def run(self, client: LangChainWrapProxy, **kwargs):
        """
        Abstract method for executing command logic.
        :param client: The LangChainWrap client.
        :param kwargs: Additional parameters for underlying models, endpoints, and frameworks.
        """
        pass

    @abstractmethod
    def get_prompt_template(self) -> BasePromptTemplate:
        """
        Abstract method for retrieving the prompt template for LLM or chat models.
        :return: The prompt template.
        """
        pass

    def output_key(self):
        """
        Get the command output_key for base class for quick debugging.
        :return: The command output key.
        """
        return {
            'session_id': self.session_id,
            'cmd_name': self.cmd_name,
            'exec_time': self.exec_time,
            # 'result': self.result,
        }

    def __str__(self):
        return (f"LangChainCommand(session_id={self.session_id}" +
                f", cmd_name={self.cmd_name}" +
                f", exec_time={self.exec_time}" +
                # f", sys_prompt={self.sys_prompt}" +
                # f", user_prompt_tmpl={self.user_prompt_tmpl}" +
                f", result={self.result}" +
                ")")

    def __repr__(self):
        return (f"LangChainCommand(session_id={self.session_id!r}" +
                f", cmd_name={self.cmd_name!r}" +
                f", exec_time={self.exec_time!r}" +
                # f", sys_prompt={self.sys_prompt!r}" +
                # f", user_prompt_tmpl={self.user_prompt_tmpl!r}" +
                f", result={self.result!r}" +
                ")")


class LangChainWrap(LangChainWrapProxy):
    """
    Client for abstracting boilerplate for supporting multiple models with LangChain.
    """
    def __init__(self,
                 *,
                 chat: BaseChatModel = None,
                 llm: BaseLLM = None,
                 ):
        """
        Construct a new instance.

        :param chat: The LangChain chat model.
        :param llm: The LangChain llm model.
        """
        if chat is None and llm is None:
            raise ValueError('either chat or llm is required')

        self.chat = chat
        self.llm = llm

    @retry_with_exponential_backoff
    def execute(self, cmd: LangChainCommand, **kwargs) -> LangChainCommand:
        """
        Submit a command for execution.
        :param cmd: the command instance.
        :param kwargs: Additional parameters for underlying models, endpoints, and frameworks.
        :return: The completed command instance.
        """
        log.debug(f"{cmd.session_id} | {cmd.cmd_name} | Request: {cmd}")

        lc_project: str | None = kwargs.pop('lc_project', None)
        with tracing_v2_enabled(lc_project):
            start_time = time.time()
            cmd_result: LangChainCommand = cmd.run(self, **kwargs)
            end_time = time.time()
            exec_time = end_time - start_time
            cmd_result.exec_time = exec_time

        log.debug(f"{cmd.session_id} | {cmd.cmd_name} | Response: {cmd_result}")

        return cmd_result
