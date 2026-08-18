# Ownership: Disha (AI Bug Detection Engine)
import os
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from services.prompt_manager import PromptManager

# Structured outputs definition using Pydantic
class AIBugReport(BaseModel):
    bug_id: str = Field(description="Unique bug identifier e.g., BUG-001, BUG-002")
    type: str = Field(description="Type of the bug (e.g., Syntax Error, Logic Error, Runtime Error, Security Vulnerability, Performance Issue, Input Validation Issue, Exception Handling Issue, API Misuse, Code Smell)")
    severity: str = Field(description="Severity: CRITICAL, HIGH, MEDIUM, LOW")
    confidence: float = Field(description="AI Confidence Score between 0.0 and 1.0")
    file: str = Field(description="Filename of the analyzed code")
    line: int = Field(description="Approximate line number of the issue")
    description: str = Field(description="Concise description of the bug")
    explanation: str = Field(description="Detailed explanation of the root cause")
    impact: str = Field(description="Potential impact of the issue on execution or security")
    suggestion: str = Field(description="Recommended fix actions")
    fixed_code: Optional[str] = Field(description="Corrected code snippet")
    test_case: Optional[str] = Field(description="Generated unit test reproducing/validating the issue")

class AIBugList(BaseModel):
    bugs: List[AIBugReport]

class AIAnalyzer:
    def __init__(self):
        # Configure OpenAI via environment variables
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = os.getenv("OPENAI_MODEL", "gpt-4o")
        
        # Initialize the LangChain ChatOpenAI client if API key is provided
        if self.api_key:
            self.llm = ChatOpenAI(
                openai_api_key=self.api_key,
                model_name=self.model_name,
                temperature=0.0,
            )
        else:
            self.llm = None
        
        self.prompt_manager = PromptManager()

    def analyze_code(self, language: str, code: str, file_name: str) -> List[Dict[str, Any]]:
        """
        Analyzes the source code to find bugs and returns a list of detected issues.
        Uses LangChain's ChatOpenAI and structured output schemas.
        """
        # If API key is missing, return a dummy mock response for demo safety
        if not self.llm:
            return self._get_mock_analysis(language, file_name)

        try:
            # 1. Load and format prompt using PromptManager
            prompt_text = self.prompt_manager.get_prompt(
                "bug_detection",
                language=language,
                code=code,
                file_name=file_name
            )

            # 2. Bind structured output parsing to our model
            structured_llm = self.llm.with_structured_output(AIBugList)

            # 3. Call the model
            response = structured_llm.invoke(prompt_text)
            
            # 4. Format Pydantic models back to standard list of dictionaries
            result = []
            for bug in response.bugs:
                result.append(bug.model_dump())
            return result

        except Exception as e:
            # Safe fallback if API call fails
            return self._get_mock_analysis(language, file_name)

    def _get_mock_analysis(self, language: str, file_name: str) -> List[Dict[str, Any]]:
        """
        Fallback mock data generator for demo/offline runs.
        """
        return [
            {
                "bug_id": "BUG-001",
                "type": "Runtime Error",
                "severity": "HIGH",
                "confidence": 0.96,
                "file": file_name,
                "line": 3,
                "description": "Possible division by zero.",
                "explanation": "The function may divide by zero when an empty list is supplied.",
                "impact": "The application may terminate with ZeroDivisionError.",
                "suggestion": "Validate the input before performing the division.",
                "fixed_code": "def calculate_average(numbers):\n    if not numbers:\n        return 0\n    return sum(numbers) / len(numbers)",
                "test_case": "def test_empty_numbers():\n    assert calculate_average([]) == 0",
                "status": "OPEN"
            }
        ]
