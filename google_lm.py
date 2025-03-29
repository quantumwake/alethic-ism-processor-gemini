import os.path
from typing import Any, List

import dotenv

import google.generativeai as genai
from ismcore.processor.base_processor_lm import BaseProcessorLM
from ismcore.processor.monitored_processor_state import MonitoredUsage
from ismcore.utils.general_utils import parse_response
from ismcore.utils.ism_logger import ism_logger

dotenv.load_dotenv()

gemini_api_key = os.environ.get('GEMINI_API_KEY', None)
genai.configure(api_key=gemini_api_key)

logging = ism_logger(__name__)
logging.info(f'**** GEMINI API KEY (last 4 chars): {gemini_api_key[-4:]} ****')


class GoogleChatCompletionProcessor(BaseProcessorLM, MonitoredUsage):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        MonitoredUsage.__init__(self, **kwargs)


    def num_tokens_from_string(self, text: str, encoding) -> int:
        num_tokens = len(encoding.encode(text))
        return num_tokens

    def num_tokens_for_chat_messages(self, messages: List[dict], encoding):
        if not messages:
            return 0

        # Initialize the tokenizer for the specific model
        # tokenizer = tiktoken.encoding_for_model(self.provider.version)

        total_tokens = 0

        for message in messages:
            # Each message is a dictionary with 'role' and 'content'
            # The API expects tokens for both the role and content
            role_tokens = encoding.encode(message['role'])
            content_tokens = encoding.encode(message['parts'])

            # Add tokens for both the role and content
            total_tokens += len(role_tokens) + len(content_tokens)

            # OpenAI's API also includes additional tokens for separators between messages
            # We can account for these with a fixed number of tokens, typically 2 tokens per message
            total_tokens += 2  # 1 token for the role and 1 token for the separator between role and content

        return total_tokens

    async def _stream(self, input_data: Any, template: str):
        raise NotImplementedError()
        # if not template:
        #     template = str(input_data)
        #
        # # rendered message we want to submit to the model
        # message_list = self.derive_messages_with_session_data_if_any(template=template, input_data=input_data)
        # # TODO FLAG: OFF history flag injected here
        # # TODO FEATURE: CONFIG PARAMETERS -> EMBEDDINGS
        #
        # # Tokenize input and count tokens
        # # input_tokens = sum([len(tiktoken.encode(message['content'])) for message in message_list])
        # encoding = tiktoken.encoding_for_model(self.provider.version)
        #
        # client = OpenAI()
        #
        # # Create a streaming completion
        # stream = client.chat.completions.create(
        #     model=self.provider.version,
        #     messages=message_list,
        #     max_tokens=4096,
        #     stream=True,  # Enable streaming
        # )
        #
        # # populate the total tokens used
        # input_token_count = self.num_tokens_for_chat_messages(message_list, encoding=encoding)
        #
        # # Iterate over the streamed responses and yield the content
        # output_data = []
        # output_token_count = 0
        # for chunk in stream:
        #     content = chunk.choices[0].delta.content
        #     if content:
        #         output_data.append(content)
        #         output_token_count += self.num_tokens_from_string(text=content, encoding=encoding)
        #         yield content
        #
        # # count the number of tokens on output text
        #
        # # add both the user and assistant generated data to the session
        # self.update_session_data(
        #     input_data=input_data,
        #     input_template=template,
        #     output_data="".join(output_data))
        #
        # await self.send_usage_input_tokens(input_token_count)
        # await self.send_usage_output_tokens(output_token_count)

    async def _execute(self, user_prompt: str, system_prompt: str, values: dict):
        messages_dict = []

        if user_prompt:
            user_prompt = user_prompt.strip()
            # messages_dict.append({
            #     "role": "user",
            #     "parts": f"{user_prompt}"
            # })

        if system_prompt:
            system_prompt = system_prompt.strip()
            # messages_dict.append({
            #     "role": "system",
            #     "parts": system_prompt
            # })

        # if not messages_dict:
        #     raise Exception(f'no prompts specified for values {values}')

        # Initialize the model with the system instruction/prompt
        model = genai.GenerativeModel(
            self.provider.version,
            system_instruction=system_prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=4096,
                temperature=0.1,
            )
        )

        response = model.generate_content(contents=user_prompt)

        await self.send_usage_input_tokens(response.usage_metadata.prompt_token_count)
        await self.send_usage_output_tokens(response.usage_metadata.candidates_token_count)
        return parse_response(raw_response=response.text)
