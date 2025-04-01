import google.generativeai as genai

# Configure the Generative AI model
API_KEY = "AIzaSyCEn5YfcEEUnKFTRhLYXO-ebLrAmSW6AUE"  # Store in environment variables
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_text(prompt: str) -> str:
    """
    Generates AI-generated content based on the given prompt.

    :param prompt: The input text prompt.
    :return: The AI-generated response as a string.
    """
    if not prompt:
        return "Error: Prompt is required."

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


