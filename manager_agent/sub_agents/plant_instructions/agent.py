from google.adk.agents import Agent

def generate_plant_care_instructions(plant_name: str, weather_report: str) -> dict:
    """
    Generate care instructions for a plant based on its name and the current weather.
    
    Args:
        plant_name (str): The name of the plant.
        weather_report (str): The human-readable weather description.
        
    Returns:
        dict: {\"status\":\"success\",\"instructions\":...} or {\"status\":\"error\",\"error_message\":...}
    """
    try:
        care_guide = (
            f"Plant: {plant_name.title()}\n"
            f"Weather: {weather_report}\n\n"
            "Care Instructions:\n"
            "- Check plant's ideal light and water needs.\n"
            "- Water based on soil moisture and recent rain.\n"
            "- Protect from extreme wind or cold as needed.\n\n"
            "Happy growing! 🌱"
        )

        return {
            "status": "success",
            "instructions": care_guide
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to generate instructions: {e}"
        }

plant_instructions = Agent(
    name="plant_instructions",
    model="gemini-2.0-flash",
    description=(
        "A friendly, expert gardening assistant that, given a plant name "
        "and a weather summary, returns tailored, actionable growing instructions."
    ),
    instruction=(
        "You are a super-kind plant-care guru. The user gives you two inputs:\n"
        "  • plant_name: plant species (for example basil, rose, cactus)\n"
        "  • weather_report: a human-readable weather summary\n\n"
        "Create a JSON dict:\n"
        "  {\"status\":\"success\",\"instructions\":<care guide string>}\n\n"
        "Make your instructions as detailed and clear as possible:\n"
        "- Explain exactly how many times per week to water based on weather and season\n"
        "- Tell them if the plant needs full sun, partial shade, or full shade\n"
        "- Mention any special care (fertilizing, pruning, repotting)\n"
        "- Use friendly language, easy growing wishes, and emoticons that match the plant (for example 😊, 🌱, 🌸)\n\n"
        "End with an encouraging sign-off like “Happy growing! 🌼”"
    ),
    tools=[generate_plant_care_instructions],
)




