# Copyright 2026 Google LLC
# Firestore read/write tools for easy_travel agent

import uuid
from typing import Any, Dict, List, Optional
from google.cloud import firestore

# Hardcoded GCP Project ID string to prevent deployment issue on Agent Platform
# where GOOGLE_CLOUD_PROJECT or default auth resolves to numeric project number.
PROJECT_ID = "qwiklabs-gcp-03-75c5785951f4"

_db: Optional[firestore.Client] = None


def get_firestore_client() -> firestore.Client:
    """Lazy initialize and return the Firestore client using hardcoded project ID."""
    global _db
    if _db is None:
        _db = firestore.Client(project=PROJECT_ID)
    return _db


def list_saved_itineraries(destination: str = "") -> List[Dict[str, Any]]:
    """List or search saved travel itineraries from the Firestore database.

    Args:
        destination: Optional destination name to filter itineraries (e.g. 'Tokyo', 'Paris').

    Returns:
        List of itinerary dictionaries with title, budget, highlights, and dietary notes.
    """
    try:
        db = get_firestore_client()
        coll_ref = db.collection("travel_itineraries")

        results = []
        if destination.strip():
            dest_term = destination.strip().title()
            docs = coll_ref.stream()
            for doc in docs:
                data = doc.to_dict()
                if dest_term.lower() in data.get("destination", "").lower() or any(
                    dest_term.lower() in tag.lower() for tag in data.get("tags", [])
                ):
                    results.append(data)
        else:
            docs = coll_ref.stream()
            for doc in docs:
                results.append(doc.to_dict())

        return results
    except Exception as e:
        return [{"error": f"Failed to list itineraries from Firestore: {str(e)}"}]


def get_itinerary_details(itinerary_id: str) -> Dict[str, Any]:
    """Retrieve full details for a specific saved itinerary from Firestore.

    Args:
        itinerary_id: Unique itinerary ID (e.g. 'tokyo-3day-food-culture', 'paris-4day-art-bakeries').

    Returns:
        Dict containing full itinerary information or error message.
    """
    try:
        db = get_firestore_client()
        doc_ref = db.collection("travel_itineraries").document(itinerary_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        return {"error": f"Itinerary with ID '{itinerary_id}' was not found in Firestore."}
    except Exception as e:
        return {"error": f"Failed to fetch itinerary from Firestore: {str(e)}"}


def save_travel_itinerary(
    destination: str,
    title: str,
    duration_days: int,
    estimated_budget_usd: float,
    highlights: List[str],
    recommended_for: str = "General Travelers",
    dietary_friendly: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Save a new travel itinerary to the Firestore database.

    Args:
        destination: Destination city or country name (e.g. 'Tokyo', 'Rome').
        title: Descriptive title for the itinerary (e.g. '3-Day Historic Rome Walking Tour').
        duration_days: Length of the trip in days.
        estimated_budget_usd: Estimated total trip budget in USD.
        highlights: Key attractions, spots, or activities included in the itinerary.
        recommended_for: Target traveler profile (e.g. 'Food Lovers', 'Families', 'Solo Travelers').
        dietary_friendly: List of dietary or allergy safety features (e.g. ['Gluten-Free Friendly', 'Nut-Free']).

    Returns:
        Dict containing the status and saved itinerary ID.
    """
    try:
        db = get_firestore_client()
        slug = destination.lower().replace(" ", "-")
        unique_suffix = str(uuid.uuid4())[:6]
        itinerary_id = f"{slug}-{duration_days}day-{unique_suffix}"

        item = {
            "itinerary_id": itinerary_id,
            "destination": destination.title(),
            "title": title,
            "duration_days": int(duration_days),
            "estimated_budget_usd": float(estimated_budget_usd),
            "highlights": highlights,
            "recommended_for": recommended_for,
            "dietary_friendly": dietary_friendly or ["General Dining"],
            "tags": [destination.lower(), f"{duration_days}day"],
        }

        db.collection("travel_itineraries").document(itinerary_id).set(item)
        return {
            "status": "success",
            "message": f"Successfully saved itinerary '{title}' to Firestore.",
            "itinerary_id": itinerary_id,
            "itinerary": item,
        }
    except Exception as e:
        return {"error": f"Failed to save itinerary to Firestore: {str(e)}"}
