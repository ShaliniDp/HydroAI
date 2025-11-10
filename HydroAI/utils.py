import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# ✅ ML Hydration Calculation
def calculate_hydration(weight, climate, activity):
    """Calculate daily hydration target (L) based on weight, climate, and activity."""
    base = weight * 35  # ml per kg
    if climate == "Hot":
        base += 500
    elif climate == "Cold":
        base -= 200

    if activity == "High":
        base += 400
    elif activity == "Medium":
        base += 200

    return round(base / 1000, 2)  # convert to liters

# ✅ Prompt Generation for GPT
def generate_prompt(age, gender, weight, activity, intake, climate):
    return (
        f"A {age}-year-old {gender.lower()} with {activity} activity weighs {weight}kg, "
        f"drank {intake}L water today, and lives in a {climate.lower()} climate. "
        f"Provide a friendly hydration reminder schedule for the remaining day, "
        f"including when and how much water to drink, with motivational tone."
    )

# ✅ GenAI API Call
def get_ai_response(prompt):
    """Send prompt to OpenAI GPT and return AI-generated reminder."""
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=120,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        # ✅ Fallback to mock reminder when API quota is hit
        if "quota" in str(e).lower():
            return "💡 [Mock Reminder] Drink 200ml now, then take small sips every hour to stay hydrated."
        return f"⚠️ AI Error: {str(e)}"
