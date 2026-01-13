"""
Llama AI Service - NLU Parser
Converts natural language to structured JSON format
No database queries, no business logic, pure NLU
"""
import json
import subprocess
from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime, timedelta


class LlamaEntity(BaseModel):
    """Entities extracted by Llama"""
    service: Optional[str] = None
    doctor: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None


class LlamaResponse(BaseModel):
    """Response from Llama NLU parser"""
    intent: str
    confidence: float
    entities: Dict[str, Any]
    raw_input: Optional[str] = None


class LlamaService:
    """
    Pure NLU (Natural Language Understanding) Service
    
    SINGLE RESPONSIBILITY: Extract intent and entities from user input
    
    Architecture:
    [User Input] → [LlamaService] → [Planner AI] → [Business Logic]
    
    This service ONLY does NLU. It does NOT:
    ❌ Know about missing slots
    ❌ Decide which slot user is trying to fill
    ❌ Generate bot responses (Chat/Planner layer handles that)
    
    It ONLY does:
    ✅ Extract intent: appointment|query|cancel|modify|other
    ✅ Extract all entities user mentioned
    ✅ Provide confidence score
    """
    
    # System prompt for NLU: Pure entity extraction, no slot-driven logic
    SYSTEM_PROMPT_NLU = """You are a professional NLU (Natural Language Understanding) parser for a dental clinic.
Your ONLY job is to extract what the user said - nothing more, nothing less.

VALID SERVICE NAMES (extract exactly as shown):
- Cleaning (teeth cleaning and polishing)
- Extraction (remove damaged tooth)
- Checkup (oral health examination)

VALID DOCTOR NAMES:
- Dr. Wang
- Dr. Chen
- Dr. Li

EXTRACTION RULES:
1. ALWAYS output ONLY valid JSON, nothing else
2. Extract ALL entities mentioned by the user
3. Set fields to null if NOT mentioned (do NOT guess)
4. Set confidence between 0.0 and 1.0
5. Extract intent from what user is doing: appointment|query|cancel|modify|other

ENTITY EXTRACTION:
- service: one of [Cleaning, Extraction, Checkup] if mentioned, else null
- doctor: one of [Dr. Wang, Dr. Chen, Dr. Li] if mentioned, else null
- date: convert to YYYY-MM-DD format if mentioned (e.g., "tomorrow" → next day), else null
- time: convert to HH:MM format (24-hour) if mentioned (e.g., "2 PM" → "14:00"), else null
- customer_name: person's name if mentioned, else null
- customer_phone: phone number if mentioned, else null
- customer_email: email if mentioned, else null

JSON Output Format (MUST MATCH EXACTLY):
{
  "intent": "appointment|query|cancel|modify|other",
  "confidence": 0.92,
  "entities": {
    "service": "Cleaning or null",
    "doctor": "Dr. Wang or null",
    "date": "YYYY-MM-DD or null",
    "time": "HH:MM or null",
    "customer_name": "string or null",
    "customer_phone": "string or null",
    "customer_email": "string or null"
  }
}

CRITICAL: Output ONLY JSON, nothing else. Do not guess or fill in missing info."""
    
    MODEL = "llama3.2:3b"
    
    @staticmethod
    def parse_user_input(user_message: str) -> LlamaResponse:
        """
        Parse user input - pure NLU only
        
        This method ONLY extracts what user said.
        It does NOT:
        ❌ Know about missing slots
        ❌ Decide which slot to fill
        ❌ Generate responses
        
        Args:
            user_message: User's natural language input
            
        Returns:
            LlamaResponse with intent and ALL extracted entities
            
        Raises:
            ValueError: If Llama returns invalid JSON
            RuntimeError: If Ollama command fails
        """
        if not user_message or not user_message.strip():
            raise ValueError("User message cannot be empty")
        
        # Build prompt - just NLU, nothing else
        prompt = f"""{LlamaService.SYSTEM_PROMPT_NLU}

User input: {user_message}

Output ONLY JSON (no explanations, no text)."""
        
        try:
            # Call Ollama with llama3.2:3b
            result = subprocess.run(
                ["ollama", "run", LlamaService.MODEL, prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                raise subprocess.CalledProcessError(
                    result.returncode,
                    "ollama",
                    stderr=result.stderr
                )
            
            # Extract JSON from output
            output = result.stdout.strip()
            
            # Clean up the JSON output
            output = LlamaService._clean_json(output)
            
            # Parse JSON
            try:
                parsed = json.loads(output)
            except json.JSONDecodeError as e:
                # Try to fix incomplete JSON (missing closing braces)
                open_braces = output.count('{')
                close_braces = output.count('}')
                
                if open_braces > close_braces:
                    output = output + '}' * (open_braces - close_braces)
                    try:
                        parsed = json.loads(output)
                    except json.JSONDecodeError:
                        raise ValueError(f"Llama returned invalid JSON: {output[:200]}...") from e
                else:
                    raise ValueError(f"Llama returned invalid JSON: {output}") from e
            
            # Extract and normalize entities
            entities = parsed.get("entities", {})
            if entities and "date" in entities and entities["date"]:
                entities["date"] = LlamaService._normalize_date(entities["date"])
            
            # Clean up null/empty strings
            for key in list(entities.keys()):
                if entities[key] == "" or entities[key] == "null":
                    entities[key] = None
            
            # Extract intent (handle pipe-separated values)
            raw_intent = parsed.get("intent", "other")
            if isinstance(raw_intent, str) and "|" in raw_intent:
                intent = raw_intent.split("|")[0].strip()
            else:
                intent = raw_intent
            
            return LlamaResponse(
                intent=intent,
                confidence=float(parsed.get("confidence", 0.5)),
                entities=entities,
                raw_input=user_message
            )
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("Llama request timed out (>30 seconds)")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Ollama error: {e.stderr}")
    
    @staticmethod
    def _clean_json(text: str) -> str:
        """
        Clean JSON output from Llama (remove comments, extra text)
        
        Args:
            text: Raw output from Llama
            
        Returns:
            Clean JSON string
        """
        # Remove leading/trailing whitespace
        text = text.strip()
        
        # Find the start of JSON (first { or [)
        json_start = text.find('{')
        if json_start == -1:
            json_start = text.find('[')
        
        if json_start != -1:
            text = text[json_start:]
        
        # Find the end of JSON (last } or ])
        json_end = max(text.rfind('}'), text.rfind(']'))
        if json_end != -1:
            text = text[:json_end + 1]
        
        # Remove JSON comments (// ... and /* ... */)
        # Remove // comments
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            # Remove // comments
            comment_index = line.find('//')
            if comment_index != -1:
                # Make sure it's not inside a string
                in_string = False
                escape_next = False
                for i, char in enumerate(line):
                    if escape_next:
                        escape_next = False
                        continue
                    if char == '\\':
                        escape_next = True
                        continue
                    if char == '"':
                        in_string = not in_string
                    if char == '/' and i + 1 < len(line) and line[i + 1] == '/' and not in_string:
                        line = line[:i]
                        break
            cleaned_lines.append(line)
        
        text = '\n'.join(cleaned_lines)
        
        # Remove /* */ comments
        while '/*' in text and '*/' in text:
            start = text.find('/*')
            end = text.find('*/', start)
            if end != -1:
                text = text[:start] + text[end + 2:]
            else:
                break
        
        # Remove trailing commas in JSON (common error)
        text = text.replace(',\n}', '\n}')
        text = text.replace(',\n]', '\n]')
        text = text.replace(', }', '}')
        text = text.replace(', ]', ']')
        
        return text.strip()
    
    @staticmethod
    def _normalize_date(date_str: Optional[str]) -> Optional[str]:
        """
        Normalize date strings like 'today', 'tomorrow' to YYYY-MM-DD format
        
        Args:
            date_str: Date string or null
            
        Returns:
            Normalized date in YYYY-MM-DD format or null
        """
        if not date_str:
            return None
        
        date_str = date_str.lower().strip()
        today = datetime.now().date()
        
        if date_str == "today":
            return today.isoformat()
        elif date_str == "tomorrow":
            return (today + timedelta(days=1)).isoformat()
        elif date_str.startswith("20") or date_str.startswith("19"):  # Already a year
            # Already in YYYY-MM-DD format, return as-is
            return date_str
        
        # Return original if we can't normalize
        return date_str


# Example usage for testing (NLU only)
if __name__ == "__main__":
    test_inputs = [
        "I want to book an appointment with Dr. Wang for teeth cleaning tomorrow at 2 PM",
        "Cancel my 10 AM appointment today",
        "What is Dr. Li's medical license?",
        "I need to reschedule my Thursday appointment to Friday afternoon",
    ]
    
    for user_input in test_inputs:
        print(f"\nUser: {user_input}")
        try:
            response = LlamaService.parse_user_input(user_input)
            print(f"Intent: {response.intent}")
            print(f"Confidence: {response.confidence}")
            print(f"Entities: {response.entities}")
        except Exception as e:
            print(f"Error: {e}")

