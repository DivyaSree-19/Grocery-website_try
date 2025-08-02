from django.shortcuts import render

# Create your views here.
'''
def nutrition(request):
    return render(request,'nutrition/sample.html')
'''

# views.py
import json
import requests
from django.shortcuts import render

# Nutrition Info from API Ninjas + USDA API for Protein & Calories
def nutrition(request):
    if request.method == 'POST':
        query = request.POST.get('query', '')
        if query:
            # API 1: API Ninjas
            api_url_1 = 'https://api.api-ninjas.com/v1/nutrition?query='
            api_request_1 = requests.get(
                api_url_1 + query,
                headers={'X-Api-Key': 'gSln0PdlZRZsGEBI79po5g==QSM7VzMuS5SulGhd'}
            )

            try:
                api_1 = json.loads(api_request_1.content)
                if api_1:
                    nutritional_info = api_1[0]

                    def get_value(key, fallback='N/A'):
                        value = nutritional_info.get(key, fallback)
                        if isinstance(value, str) and 'only available' in value.lower():
                            return fallback
                        return value

                    # From API Ninjas
                    carbohydrates = get_value('carbohydrates_total_g', 'N/A')
                    cholesterol = get_value('cholesterol_mg', 'N/A')
                    saturated_fat = get_value('fat_saturated_g', 'N/A')
                    total_fat = get_value('fat_total_g', 'N/A')
                    fiber = get_value('fiber_g', 'N/A')
                    potassium = get_value('potassium_mg', 'N/A')
                    sodium = get_value('sodium_mg', 'N/A')
                    sugar = get_value('sugar_g', 'N/A')

                    # ------------------------
                    # USDA API for Protein & Calories
                    # ------------------------
                    usda_api_key = "seYHUXci3PrKLYUwivvV916s2WTJBXLEsi0NH2gP"
                    usda_url = "https://api.nal.usda.gov/fdc/v1/foods/search"
                    params = {
                        'query': query,
                        'api_key': usda_api_key,
                        'pageSize': 1
                    }
                    protein = 'N/A'
                    calories = 'N/A'

                    usda_response = requests.get(usda_url, params=params)
                    if usda_response.status_code == 200:
                        usda_data = usda_response.json()
                        if usda_data.get('foods'):
                            food_item = usda_data['foods'][0]
                            nutrients = {n['nutrientName']: n['value'] for n in food_item.get('foodNutrients', [])}

                            protein = nutrients.get('Protein', 'N/A')
                            calories = nutrients.get('Energy', 'N/A')
                        else:
                            print("No USDA data found.")
                    else:
                        print("USDA API failed")

                    # Final context
                    context = {
                        'query': query,
                        'carbohydrates': carbohydrates,
                        'cholesterol': cholesterol,
                        'saturated_fat': saturated_fat,
                        'total_fat': total_fat,
                        'fiber': fiber,
                        'potassium': potassium,
                        'sodium': sodium,
                        'sugar': sugar,
                        'protein': protein,
                        'calories': calories,
                    }

                else:
                    context = {'query': query, 'error': 'No data found for this product.'}

            except Exception as e:
                context = {'query': query, 'error': 'Error in fetching data from APIs.'}
                print(e)

            return render(request, 'nutrition/sample.html', context)

        else:
            return render(request, 'nutrition/sample.html', {'query': ''})
    else:
        return render(request, 'nutrition/sample.html', {'query': ''})

