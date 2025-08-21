"""
AI Destinations Service - OpenAI integration for destination descriptions and funny facts.
"""
import os
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AIDestinationsService:
    """Service for getting destination descriptions and funny facts using OpenAI."""
    
    def __init__(self):
        """Initialize the AI service with OpenAI client."""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # Using OpenAI's mini model
    
    def get_destinations_info(self, destinations: List[str]) -> Dict[str, str]:
        """
        Get descriptions and funny facts for a list of destinations.
        
        Args:
            destinations: List of destination names (e.g., ["London", "Barcelona"])
            
        Returns:
            Dictionary with destination names as keys and descriptions as values
        """
        if not destinations:
            return {}
        
        try:
            # Create the prompt in Polish
            destinations_text = ", ".join(destinations)
            prompt = f"""
            Dla następujących miast/destynacji: {destinations_text}
            
            Dla każdego miejsca napisz krótki opis (3-5 zdania) oraz jeden zabawny/ciekawy fakt o tym miejscu.
            
            Odpowiedź sformatuj dokładnie w następującym formacie:
            [krótki opis miejsca rozpoczynający się od nazwy miejsca] [zabawny fakt o miejscu]
            
            Każde miejsce w osobnej linii. Odpowiadaj tylko po polsku.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "Jesteś pomocnym asystentem, który udziela informacji o miejscach podróży po polsku. Jesteś precyzyjny, zwięzły i zabawny w swoich odpowiedziach."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            # Parse the response
            content = response.choices[0].message.content.strip()
            return self._parse_response(content, destinations)
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            # Return fallback responses
            return {dest: f"{dest}: Nie udało się pobrać informacji o tym miejscu." for dest in destinations}
    
    def _parse_response(self, content: str, original_destinations: List[str]) -> Dict[str, str]:
        """
        Parse the OpenAI response into a dictionary.
        
        Args:
            content: Raw response from OpenAI
            original_destinations: Original list of destinations for fallback
            
        Returns:
            Dictionary with destination names as keys and descriptions as values
        """
        result = {}
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if ':' in line and line:
                # Split on first occurrence of ':'
                parts = line.split(':', 1)
                if len(parts) == 2:
                    city = parts[0].strip()
                    description = parts[1].strip()
                    result[city] = f"{city}: {description}"
        
        # Ensure we have responses for all requested destinations
        for dest in original_destinations:
            found = False
            for key in result.keys():
                if dest.lower() in key.lower() or key.lower() in dest.lower():
                    found = True
                    break
            
            if not found:
                result[dest] = f"{dest}: Piękne miejsce warte odwiedzenia."
        
        return result
    
    def format_response(self, destinations_info: Dict[str, str]) -> str:
        """
        Format the response in the requested format.
        
        Args:
            destinations_info: Dictionary with destination info
            
        Returns:
            Formatted string with destinations and descriptions
        """
        return '\n'.join(destinations_info.values())


def main():
    """Example usage of the AI Destinations Service."""
    try:
        # Example destinations from the flights data
        example_destinations = ["London", "Barcelona", "Paris", "Rome"]
        
        ai_service = AIDestinationsService()
        destinations_info = ai_service.get_destinations_info(example_destinations)
        formatted_response = ai_service.format_response(destinations_info)
        
        print("=== AI Destinations Info ===")
        print(formatted_response)
        
    except Exception as e:
        print(f"Error in AI Destinations Service: {e}")


if __name__ == "__main__":
    main()
