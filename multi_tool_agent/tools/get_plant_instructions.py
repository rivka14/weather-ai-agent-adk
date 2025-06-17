# multi_tool_agent/tools/get_plant_instructions.py
from google.cloud import aiplatform
from google.cloud.aiplatform.preview.language_models import TextGenerationModel

# Initialize AI Platform (uses Application Default Credentials under the hood)
aiplatform.init(project="YOUR_GCP_PROJECT_ID", location="us-central1")

# Load the Gemini model from the Model Garden
model = TextGenerationModel.from_pretrained("gemini-2.0-flash")

def get_plant_instructions(plant_name: str) -> dict:
    """
    Generates detailed care instructions for a specified plant using the Gemini model.
    """
    # Build the prompt dynamically
    prompt = (
        f"Provide detailed care instructions for the houseplant '{plant_name}'. "
        "Include light requirements, watering frequency, soil recommendations, and common pitfalls."
    )
    try:
        # Call the model via the SDK
        response = model.predict(
            prompt=prompt,
            temperature=0.7,
            max_output_tokens=300
        )
        # Return the successful response
        return {
            "status": "success",
            "plant": plant_name,
            "instructions": response.text,
        }
    except Exception as e:
        # Return error information
        return {
            "status": "error",
            "error_message": str(e),
        }
