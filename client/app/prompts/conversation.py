from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser



template = """
        <|begin_of_text|>
        <|start_header_id|>system<|end_header_id|>
        "You are an assistant for question-answering tasks. Use the following pieces of retrieved context & chat history to precisely answer the question in 200 words. If you don't know the answer, say that you don't know. Use three sentences maximum and keep the answer concise.\n"
        context: {system_prompt}
        chat_history: {chat_history} <|eot_id|>
        <|start_header_id|>user<|end_header_id|>
        {user_prompt}<|eot_id|>
        <|start_header_id|>assistant<|end_header_id|>
        """

basic_prompt = PromptTemplate(template=template,  input_variables=["system_prompt", "user_prompt", "chat_history"] )