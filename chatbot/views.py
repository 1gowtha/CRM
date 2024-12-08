from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        try:
            # Parse JSON body
            data = json.loads(request.body)
            user_message = data.get('message', '').strip().lower()

            # Example bot response logic
            if "hello" in user_message:
                bot_response = "Hi there! How can I assist you today?"
            else:
                bot_response = "I'm not sure how to respond to that."

            return JsonResponse({'response': bot_response})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
