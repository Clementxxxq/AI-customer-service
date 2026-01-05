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
    """Service to call Llama3.2:3b for NLU"""
    
    # System prompt for Llama - strict NLU only
    SYSTEM_PROMPT = """You are a strict NLU (Natural Language Understanding) parser.
Your ONLY job is to convert user natural language into JSON format.

Rules (MUST FOLLOW):
- Extract user intent: appointment, query, cancel, modify, other
- Extract entities: doctor name, service name, date, time, phone, email
- ALWAYS output ONLY valid JSON
- Do NOT query databases, make decisions, or provide advice
- Set fields to null if not mentioned in user input
- Set confidence between 0.0 and 1.0
- Do NOT add any text before or after the JSON

Output JSON schema (EXACT FORMAT):
{
  "intent": "appointment|query|cancel|modify|other",
  "confidence": 0.95,
  "entities": {
    "service": "string or null",
    "doctor": "string or null",
    "date": "YYYY-MM-DD or null",
    "time": "HH:MM or null",
    "customer_name": "string or null",
    "customer_phone": "string or null",
    "customer_email": "string or null"
  }
}

CRITICAL: Output ONLY JSON, nothing else."""
    
    MODEL = "llama3.2:3b"
    
    @staticmethod
    def parse_user_input(user_message: str) -> LlamaResponse:
        """
        Parse user input using Llama to extract intent and entities
        
        Args:
            user_message: User's natural language input
            
        Returns:
            LlamaResponse with parsed intent and entities
            
        Raises:
            ValueError: If Llama returns invalid JSON
            subprocess.CalledProcessError: If Ollama command fails
        """
        if not user_message or not user_message.strip():
            raise ValueError("User message cannot be empty")
        
        # Build prompt
        prompt = f"""{LlamaService.SYSTEM_PROMPT}

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
                raise ValueError(f"Llama returned invalid JSON: {output}") from e
            
            # Normalize date if it's "today" or "tomorrow"
            entities = parsed.get("entities", {})
            if entities and "date" in entities:
                entities["date"] = LlamaService._normalize_date(entities["date"])
            
            # Convert empty strings and "null" strings to None in entities
            for key in entities:
                if entities[key] == "" or entities[key] == "null":
                    entities[key] = None
            
            # Build response - pass entity dict directly, not AIEntity object
            return LlamaResponse(
                intent=parsed.get("intent", "other"),
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
    
    @staticmethod
    def generate_bot_response(intent: str, entities: Dict[str, Any]) -> str:
        """
        Generate a natural language response based on parsed intent and entities
        
        Args:
            intent: The parsed intent
            entities: The extracted entities
            
        Returns:
            Natural language response string
        """
        if intent == "appointment":
            service = entities.get("service") or "an appointment"
            doctor = entities.get("doctor") or "a doctor"
            date = entities.get("date") or "at your preferred time"
            
            return f"I understand you want to book {service} with {doctor} on {date}. Let me connect you with our scheduling system."
        
        elif intent == "cancel":
            date = entities.get("date") or "a scheduled appointment"
            time = entities.get("time") or ""
            
            if time:
                return f"I see you want to cancel your appointment on {date} at {time}. I'll process the cancellation."
            return f"I see you want to cancel your appointment. Let me help with that."
        
        elif intent == "query":
            doctor = entities.get("doctor")
            service = entities.get("service")
            
            if doctor:
                return f"You're asking about {doctor}. Let me fetch that information for you."
            elif service:
                return f"You want to know more about {service}. Here's what I can tell you."
            return "I understand your question. Let me find that information."
        
        elif intent == "modify":
            return "I see you want to modify your appointment. Let me help you reschedule."
        
        else:  # "other"
            return "I understood your message. How can I assist you with our dental services?"


# Example usage for testing
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
            bot_response = LlamaService.generate_bot_response(response.intent, response.entities)
            print(f"Bot: {bot_response}")
        except Exception as e:
            print(f"Error: {e}")
