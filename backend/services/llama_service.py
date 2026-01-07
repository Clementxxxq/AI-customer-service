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
    
    # System prompt for Llama - slot-driven NLU
    # Modified for professional customer service excellence
    SYSTEM_PROMPT = """You are a professional NLU (Natural Language Understanding) parser for a dental clinic customer service system.
Your job is to accurately understand customer needs and extract information for booking appointments with excellent customer focus.

VALID SERVICE NAMES (extract exactly as shown):
- Cleaning (teeth cleaning and polishing)
- Extraction (remove damaged tooth)
- Checkup (oral health examination)

VALID DOCTOR NAMES:
- Dr. Wang
- Dr. Chen
- Dr. Li

CUSTOMER INFORMATION EXTRACTION:
- customer_name: Look for names (e.g., "John", "Zhang Wei", "My name is...")
- customer_phone: Look for phone numbers (e.g., "+86 123456789", "13912345678")
- customer_email: Look for email addresses (e.g., "user@example.com")

Rules (MUST FOLLOW):
1. You will receive MISSING SLOTS - these are the slots the system is asking about
2. Look at the user input and decide which missing slot it's most likely filling
3. Extract ONLY the value for that slot (or the primary slot if multiple)
4. Do NOT try to extract fields that aren't in the missing slots list
5. ALWAYS output ONLY valid JSON
6. Set confidence between 0.0 and 1.0
7. If you're unsure which slot the input fills, return target_slot: "unknown"

EXTRACTION GUIDELINES:
- For dates: convert "next Monday", "tomorrow", "2026-01-15", "Wed", "3 days from now" to YYYY-MM-DD format
- For times: convert "9 AM", "14:30", "3 o'clock" to HH:MM format (24-hour)
- For names: extract the person's name (can be first name only or full name)
- For phone: extract just the number part, remove spaces and special formatting
- For email: extract the full email address
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

CRITICAL: Output ONLY JSON, nothing else. Prioritize accuracy and customer service quality."""
    
    MODEL = "llama3.2:3b"
    
    @staticmethod
    def parse_user_input(user_message: str, context: Optional[Dict[str, Any]] = None, missing_slots: Optional[list] = None) -> LlamaResponse:
        """
        Parse user input using slot-driven approach
        
        Args:
            user_message: User's natural language input
            context: Dict with already-collected entities: {"doctor": "Dr. Wang", "service": None, ...}
            missing_slots: List of slots still needed (in priority order): ["service", "date", "time"]
                          If provided, NLU only extracts these slots and identifies which one user is filling
            
        Returns:
            LlamaResponse with target_slot and value, instead of full entities
            
        Raises:
            ValueError: If Llama returns invalid JSON
            subprocess.CalledProcessError: If Ollama command fails
        """
        if not user_message or not user_message.strip():
            raise ValueError("User message cannot be empty")
        
        # Build prompt with context if provided
        context_str = ""
        if context:
            # Only include fields that have been collected
            collected = {k: v for k, v in context.items() if v is not None}
            if collected:
                context_str = f"""

CURRENT BOOKING INFORMATION ALREADY COLLECTED:
{json.dumps(collected, indent=2, ensure_ascii=False)}"""
        
        # Add missing slots guidance (slot-driven mode)
        slots_str = ""
        if missing_slots:
            slots_str = f"""

MISSING SLOTS (ask user about these):
{', '.join(missing_slots)}

Your task:
1. Identify which slot the user input is trying to fill
2. Extract the value for that target slot ONLY
3. Ignore other fields not in missing slots
4. Return: target_slot, value, confidence"""
        
        # Build prompt
        prompt = f"""{LlamaService.SYSTEM_PROMPT}{context_str}{slots_str}

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
                # Count open and close braces
                open_braces = output.count('{')
                close_braces = output.count('}')
                
                if open_braces > close_braces:
                    # Add missing closing braces
                    output = output + '}' * (open_braces - close_braces)
                    try:
                        parsed = json.loads(output)
                    except json.JSONDecodeError:
                        raise ValueError(f"Llama returned invalid JSON: {output[:200]}...") from e
                else:
                    raise ValueError(f"Llama returned invalid JSON: {output}") from e
            
            # Handle slot-driven mode response
            if missing_slots and "target_slot" in parsed:
                # Slot-driven: extract only the target field
                target_slot = parsed.get("target_slot", "unknown")
                value = parsed.get("value")
                
                # Normalize value based on slot type
                if target_slot == "date" and value:
                    value = LlamaService._normalize_date(value)
                
                # Convert to entities dict for compatibility
                entities = {}
                if target_slot != "unknown" and value is not None and value != "":
                    entities[target_slot] = value
                
                return LlamaResponse(
                    intent="appointment",
                    confidence=float(parsed.get("confidence", 0.7)),
                    entities=entities,
                    raw_input=user_message
                )
            else:
                # Full entity extraction mode (backward compatibility)
                entities = parsed.get("entities", {})
                if entities and "date" in entities:
                    entities["date"] = LlamaService._normalize_date(entities["date"])
                
                # Convert empty strings and "null" strings to None in entities
                for key in entities:
                    if entities[key] == "" or entities[key] == "null":
                        entities[key] = None
                
                # Extract intent - handle cases like "appointment|query" by taking the first one
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
    
    @staticmethod
    def generate_bot_response(intent: str, entities: Dict[str, Any]) -> str:
        """
        Generate a natural language response as a professional customer service representative.
        Responses are warm, helpful, attentive, and customer-focused.
        
        Args:
            intent: The parsed intent
            entities: The extracted entities
            
        Returns:
            Natural language response string in professional service representative style
        """
        if intent == "appointment":
            service = entities.get("service") or "an appointment"
            doctor = entities.get("doctor") or "your preferred dentist"
            date = entities.get("date") or "your preferred date"
            
            return f"Perfect! I'd be delighted to help you book {service} with {doctor} on {date}. Let me confirm the details to ensure everything is just right for you."
        
        elif intent == "cancel":
            date = entities.get("date") or "your scheduled appointment"
            time = entities.get("time") or ""
            
            if time:
                return f"I understand you'd like to cancel your appointment on {date} at {time}. I'll be happy to help process that for you right away."
            return f"I completely understand. I'll help you cancel your appointment immediately. Just let me gather the details."
        
        elif intent == "query":
            doctor = entities.get("doctor")
            service = entities.get("service")
            
            if doctor:
                return f"Thank you for your interest! I'd be happy to share more information about {doctor}. Let me get you all the details about their background and expertise."
            elif service:
                return f"Great question! I'm glad you're interested in learning more about {service}. Let me provide you with comprehensive information to help you make the best decision."
            return "Thank you for reaching out with your question. I'm here to help and will find exactly what you need."
        
        elif intent == "modify":
            return "I completely understand that schedules change! I'm here to help you reschedule your appointment to a more convenient time. Let's find the perfect slot for you."
        
        else:  # "other"
            return "Thank you for reaching out! I'm here to help you with all your dental care needs. What can I assist you with today?"


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
