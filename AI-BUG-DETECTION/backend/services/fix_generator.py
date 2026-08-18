# Ownership: Disha (AI Bug Detection Engine)
import os
from typing import Dict, Any
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from services.prompt_manager import PromptManager

class AIFixReport(BaseModel):
    fixed_code: str = Field(description="The complete corrected source code block")
    explanation: str = Field(description="An explanation of what changes were made and why they fix the bug")

class FixGenerator:
    """
    Generates optimized bug corrections and fixes using LangChain and ChatOpenAI.
    """
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = os.getenv("OPENAI_MODEL", "gpt-4o")
        
        if self.api_key:
            self.llm = ChatOpenAI(
                openai_api_key=self.api_key,
                model_name=self.model_name,
                temperature=0.0,
            )
        else:
            self.llm = None
            
        self.prompt_manager = PromptManager()

    def generate_fix(self, language: str, original_code: str, bug_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Queries ChatOpenAI via LangChain to generate a code fix and explanation.
        """
        if not self.llm:
            return self._get_mock_fix(original_code)

        try:
            # 1. Format the generation prompt
            prompt_text = self.prompt_manager.get_prompt(
                "fix_generation",
                language=language,
                code=original_code,
                line=bug_details.get("line", 1),
                bug_type=bug_details.get("type", "Logic Error"),
                description=bug_details.get("description", "Potential bug")
            )

            # 2. Bind structured output model
            structured_llm = self.llm.with_structured_output(AIFixReport)

            # 3. Call model
            response = structured_llm.invoke(prompt_text)

            return response.model_dump()

        except Exception as e:
            return self._get_mock_fix(original_code)

    def _get_mock_fix(self, original_code: str) -> Dict[str, Any]:
        """
        Mock fallback handler for fix generation.
        """
        return {
            "fixed_code": original_code,
            "explanation": "No automated fix generated (offline mock mode active)."
        }
