# Copyright 2026 Google LLC
# Seed script for Firestore collection 'travel_itineraries'

from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-03-75c5785951f4"

db = firestore.Client(project=PROJECT_ID)
collection_ref = db.collection("travel_itineraries")

SEED_ITINERARIES = [
    {
        "itinerary_id": "tokyo-3day-food-culture",
        "destination": "Tokyo",
        "title": "3-Day Tokyo Historic Temples & Street Food Tour",
        "duration_days": 3,
        "estimated_budget_usd": 600.0,
        "highlights": ["Senso-ji Temple", "Tsukiji Outer Food Market", "Shibuya Crossing", "Meiji Shrine"],
        "recommended_for": "Food Lovers, Cultural Explorers, Budget Travelers",
        "dietary_friendly": ["Vegetarian Options", "Nut-Free Options", "Halal Options"],
        "tags": ["tokyo", "japan", "food", "temples", "budget"],
    },
    {
        "itinerary_id": "paris-4day-art-bakeries",
        "destination": "Paris",
        "title": "4-Day Paris Art, Museums & Artisan Bakery Trail",
        "duration_days": 4,
        "estimated_budget_usd": 850.0,
        "highlights": ["Eiffel Tower & Champ de Mars", "Louvre Museum", "Le Marais Bakery Walk", "Montmartre Views"],
        "recommended_for": "Art & History Buffs, Pastry Enthusiasts, Couples",
        "dietary_friendly": ["Gluten-Free Bakeries", "Dairy-Free Options"],
        "tags": ["paris", "france", "art", "museums", "bakeries"],
    },
    {
        "itinerary_id": "kyoto-3day-zen-gardens",
        "destination": "Kyoto",
        "title": "3-Day Kyoto Zen Temples & Bamboo Forest Walk",
        "duration_days": 3,
        "estimated_budget_usd": 550.0,
        "highlights": ["Fushimi Inari Shrine", "Arashiyama Bamboo Grove", "Kinkaku-ji Golden Pavilion", "Gion Evening Walk"],
        "recommended_for": "Nature Seekers, Photography, Serene Escapes",
        "dietary_friendly": ["Vegetarian / Shojin Ryori", "Vegan Friendly"],
        "tags": ["kyoto", "japan", "nature", "temples", "zen"],
    },
    {
        "itinerary_id": "nyc-3day-landmarks-broadway",
        "destination": "New York",
        "title": "3-Day NYC Iconic Sights, Central Park & Broadway",
        "duration_days": 3,
        "estimated_budget_usd": 900.0,
        "highlights": ["Central Park Walk", "Statue of Liberty Ferry", "Times Square & Broadway Show", "High Line Park"],
        "recommended_for": "First-Time Visitors, Theater Fans, Fast-Paced Explorers",
        "dietary_friendly": ["Kosher Friendly", "Vegan Options", "Allergy-Aware Dining"],
        "tags": ["nyc", "new york", "broadway", "city", "landmarks"],
    },
]


def seed_database():
    print(f"Seeding Firestore collection 'travel_itineraries' in project {PROJECT_ID}...")
    for item in SEED_ITINERARIES:
        doc_ref = collection_ref.document(item["itinerary_id"])
        doc_ref.set(item)
        print(f"  ✓ Seeded itinerary: {item['itinerary_id']} ({item['title']})")
    print("✨ Firestore seeding completed successfully!")


if __name__ == "__main__":
    seed_database()
