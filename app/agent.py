# ruff: noqa
import datetime
from typing import Dict, List, Any
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types

from app.firestore_tools import (
    get_itinerary_details,
    list_saved_itineraries,
    save_travel_itinerary,
)

MODEL = "gemini-3.6-flash"


async def generate_memories_callback(callback_context: CallbackContext):
    """WRITE: after each turn, send the session to Memory Bank for extraction."""
    try:
        await callback_context.add_session_to_memory()
    except Exception:
        pass
    return None


def search_attractions(destination: str, category: str = "general") -> Dict[str, Any]:
    """Search for top attractions and activities in a travel destination.

    Args:
        destination: Name of the destination city or country (e.g. 'Tokyo', 'Paris', 'New York').
        category: Category of activities (e.g. 'sightseeing', 'food', 'culture', 'nature', 'budget').

    Returns:
        Dict containing top attractions, recommended duration, and tips.
    """
    dest_lower = destination.lower()
    if "tokyo" in dest_lower:
        return {
            "destination": "Tokyo, Japan",
            "attractions": [
                {"name": "Senso-ji Temple & Nakamise Street", "type": "Culture/History", "est_cost": "$0"},
                {"name": "Tsukiji Outer Market Food Tour", "type": "Food", "est_cost": "$25"},
                {"name": "Shibuya Crossing & Skytree", "type": "Sightseeing", "est_cost": "$18"},
            ],
            "best_season": "Spring (Cherry Blossom) or Autumn",
        }
    elif "paris" in dest_lower:
        return {
            "destination": "Paris, France",
            "attractions": [
                {"name": "Eiffel Tower & Champ de Mars", "type": "Landmark", "est_cost": "$30"},
                {"name": "Louvre Museum", "type": "Art/History", "est_cost": "$22"},
                {"name": "Le Marais Walking & Bakery Tour", "type": "Food/Culture", "est_cost": "$15"},
            ],
            "best_season": "Spring (May) or Autumn (September)",
        }
    return {
        "destination": destination.title(),
        "attractions": [
            {"name": f"Historic Old Town of {destination.title()}", "type": "Culture", "est_cost": "Free"},
            {"name": f"Local Central Market & Food Hall", "type": "Culinary", "est_cost": "$15-$30"},
            {"name": f"Scenic City Viewpoint / Park", "type": "Sightseeing", "est_cost": "Free"},
        ],
        "best_season": "Year-round",
    }


def estimate_trip_budget(days: int, daily_budget_usd: float, number_of_travelers: int = 1) -> Dict[str, Any]:
    """Calculate and breakdown the estimated travel budget.

    Args:
        days: Duration of the trip in days.
        daily_budget_usd: Estimated daily spending budget per person in USD.
        number_of_travelers: Number of people traveling together.

    Returns:
        Dict containing total cost breakdown by category (lodging, food, activities, emergency buffer).
    """
    subtotal = days * daily_budget_usd * number_of_travelers
    lodging = round(subtotal * 0.40, 2)
    food = round(subtotal * 0.35, 2)
    activities = round(subtotal * 0.15, 2)
    buffer = round(subtotal * 0.10, 2)

    return {
        "days": days,
        "travelers": number_of_travelers,
        "daily_per_person_usd": daily_budget_usd,
        "total_estimated_usd": round(subtotal, 2),
        "breakdown": {
            "lodging_usd": lodging,
            "food_usd": food,
            "activities_usd": activities,
            "emergency_buffer_usd": buffer,
        },
    }


def get_destination_weather(destination: str) -> Dict[str, Any]:
    """Get the current weather and packing advice for a destination.

    Args:
        destination: Destination city or location name.

    Returns:
        Dict with weather condition, temperature, and packing suggestions.
    """
    dest_lower = destination.lower()
    if "tokyo" in dest_lower:
        return {"destination": "Tokyo", "condition": "Mild & Clear", "temp_f": 65, "packing": "Light jacket and comfortable walking shoes."}
    elif "paris" in dest_lower:
        return {"destination": "Paris", "condition": "Partly Cloudy", "temp_f": 58, "packing": "Layered clothing and an umbrella."}
    return {"destination": destination.title(), "condition": "Sunny & Pleasant", "temp_f": 72, "packing": "Sunglasses, sunscreen, and light wear."}


root_agent = Agent(
    name="easy_travel",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are 'easy_travel', a friendly and expert AI Travel Concierge. "
        "Your goal is to help users plan amazing, stress-free trips.\n\n"
        "ALLERGY & DIETARY SAFETY MANDATE:\n"
        "- Actively identify and remember all user allergies (e.g., peanuts, gluten, shellfish, dairy, pollen, latex, insect stings, medications) and dietary restrictions mentioned by the user.\n"
        "- Ensure every dining option, food tour, hotel amenity, and activity recommendation strictly accounts for and avoids the user's reported allergies.\n"
        "- Whenever preloaded memories contain allergy information, explicitly acknowledge allergy-safe options when presenting itineraries or dining suggestions.\n\n"
        "DATABASE & ITINERARY MANAGEMENT:\n"
        "- Use `list_saved_itineraries` to browse or search stored itineraries in the database.\n"
        "- Use `get_itinerary_details` to retrieve full details for a saved itinerary.\n"
        "- Use `save_travel_itinerary` whenever the user asks to save a newly planned trip or itinerary to their database.\n\n"
        "Always remember the user's stated travel preferences, budget, and facts from previous conversations to personalize your responses. "
        "Always recommend exciting itineraries, provide accurate budget breakdowns using `estimate_trip_budget`, "
        "suggest top attractions using `search_attractions`, and offer helpful packing/weather tips with `get_destination_weather`. "
        "Maintain an encouraging, well-structured, and helpful tone."
    ),
    tools=[
        PreloadMemoryTool(),
        search_attractions,
        estimate_trip_budget,
        get_destination_weather,
        list_saved_itineraries,
        get_itinerary_details,
        save_travel_itinerary,
    ],
    after_agent_callback=generate_memories_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)


