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

from langchain_core.prompts import PromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage
from interacticore import InteractiClient, InteractiCommand
from langchain_core.output_parsers.transform import BaseCumulativeTransformOutputParser


class LlmCommand(InteractiCommand):
    """
    Command object for LLM Model chain invocations.
    """

    def __init__(self,
                 *,
                 session_id: str = None,
                 cmd_name: str = None,
                 sys_prompt: str = None,
                 user_prompt_tmpl: str = None,
                 output_parser: BaseCumulativeTransformOutputParser = None,
                 inputs: dict = None,
                 ):
        """
        Construct a new instance.
        :param session_id: The session ID.
        :param cmd_name: The command name.
        :param sys_prompt: The system prompt.
        :param user_prompt_tmpl: The user prompt template.
        :param output_parser: The output parser.
        """
        super().__init__(
            session_id=session_id,
            cmd_name=cmd_name,
            sys_prompt=sys_prompt,
            user_prompt_tmpl=user_prompt_tmpl,
            output_parser=output_parser,
        )
        self.inputs: dict = inputs

    def get_prompt_template(self):
        return PromptTemplate.from_messages(
            [
                SystemMessage(content=self.sys_prompt),
                HumanMessagePromptTemplate.from_template(self.user_prompt_tmpl),
            ]
        )

    def run(self, client: InteractiClient, **kwargs) -> InteractiCommand:
        base_chain = self.get_prompt_template() | client.llm | self.output_parser

        base_chain_result = base_chain.invoke({
            **self.inputs,
            **kwargs,
        })
        self.result = base_chain_result
        return self

    def __str__(self):
        return (f"LlmCommand(super={super().__str__()}" +
                # f", field={self.field}" +
                ")")

    def __repr__(self):
        return (f"LlmCommand(super={super().__repr__()}" +
                # f", field={self.field!r}" +
                ")")
