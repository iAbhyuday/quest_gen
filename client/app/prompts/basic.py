from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field






# Define your desired data structure.
class Question(BaseModel):
    topic: str = Field(description="topic of the question.")
    question: str = Field(description="question asked.")
    answer: str = Field(description="correct option.")
    explain: str = Field(description="explaination to the answer.")
parser = JsonOutputParser(pydantic_object=Question)

template = """
        <|begin_of_text|>
        <|start_header_id|>system<|end_header_id|>
        
        context: {system_prompt}
        topic: {topic}
        
        You are an helpful assistant. Your goal is to formulate non-trivial questions to test candidate understanding on topics based on specified context in given question format:
        {question_type}<|eot_id|>
        
        <|start_header_id|>user<|end_header_id|>
        Design a new question with option {option} to be correct<|eot_id|>
        <|start_header_id|>assistant<|end_header_id|>
        """
inst = parser.get_format_instructions()
basic_prompt = PromptTemplate(template=template,  input_variables=["subject", "question_type", "system_prompt", "topics"] )