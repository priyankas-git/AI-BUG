# Ownership: Disha (AI Bug Detection Engine)
import os

class PromptManager:
    """
    Loads and formats prompts from the backend/prompts/ directory.
    """
    def __init__(self, prompts_dir: str = None):
        if prompts_dir is None:
            # Default directory structure setup
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.prompts_dir = os.path.join(base_dir, "prompts")
        else:
            self.prompts_dir = prompts_dir

    def get_prompt(self, prompt_name: str, **kwargs) -> str:
        """
        Reads prompt file and formats it using keyword arguments.
        """
        file_path = os.path.join(self.prompts_dir, f"{prompt_name}.txt")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Prompt file not found at {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        return content.format(**kwargs) if kwargs else content
