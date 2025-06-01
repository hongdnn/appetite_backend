# src/llm_model/llm_tools.py

import httpx
from typing import Optional
from langchain.tools import tool, Tool
from src.infrastructure.config import Config
from src.models.food import FoodCategory

API_BASE_URL = Config.API_BASE_URL

def get_headers() -> dict:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {Config.AGENT_AUTH_TOKEN}"
    }
    return headers


@tool()
async def search_food(food_name: str, category: Optional[str] = None) -> str:
    """Search for food items by name or category."""
    try:
        params = {"limit": 3, "page": 1}
        if category:
            params["category"] = category
        if food_name:
            params["input"] = food_name

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/foods/",
                params=params,
                headers=get_headers(),
                timeout=10.0
            )

        result = response.json()
        if result.get('status') == 0:
            foods = result.get('data', [])
            if foods:
                food_list = [
                    f"- {food.get('name', 'Unknown')} (ID: {food.get('id', 'N/A')})"
                    for food in foods
                ]
                print("food_list:", food_list)
                return f"Found {len(foods)} foods:\n" + "\n".join(food_list)
            return "No foods found matching your criteria."
        return "Error searching for foods."
    except Exception as e:
        print(f"Error in search_food tool: {str(e)}")
        return "Error searching for foods."


@tool()
async def get_food_detail(food_id: str) -> str:
    """Get detailed information about a specific food item using its ID.
    If the food ID is not provided, using food ID of the recent food name that user asked for.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{API_BASE_URL}/food/{food_id}",
                headers=get_headers(),
                timeout=10.0
            )

        result = response.json()
        if result['status'] == 0:
            food = result['data']
            name = food['name']
            description = food.get('description', 'No description available')

            category_enum = FoodCategory(food['category'])
            category = category_enum.name.lower()

            ingredients_data = food.get('ingredients', [])
            ingredients_str = (
                ", ".join(ingredient['name'] for ingredient in ingredients_data)
                if ingredients_data else "No ingredients listed."
            )

            return (
                f"🍽️ **Food Details**:\n"
                f"- Name: {name}\n"
                f"- Category: {category}\n"
                f"- Description: {description}\n"
                f"- Ingredients: {ingredients_str}"
            )
        elif result.get('status') == 1:
            return "Food not found. Please check and try again."
        return "Error retrieving food details."
    except Exception as e:
        print(f"Error in get_food_detail tool: {str(e)}")
        return "Error retrieving food details."

def get_tools() -> list[Tool]:
    return [
        search_food,
        get_food_detail,
    ]