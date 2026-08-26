from django.shortcuts import render
from django.http import JsonResponse

from .logic import (
    generate_password,
    calculate_strength,
    estimate_crack_time,
    validate_params,
)


def home(request):
    return render(request, 'index.html')


def generate_password_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        length = int(request.POST.get('length', 16))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid length value'}, status=400)

    selected_types = request.POST.getlist('char_types[]')
    exclude_ambiguous = request.POST.get('exclude_ambiguous') == 'true'

    errors = validate_params(length, selected_types)
    if errors:
        return JsonResponse({'error': ' '.join(errors)}, status=400)

    password, error = generate_password(length, selected_types, exclude_ambiguous)
    if error:
        return JsonResponse({'error': error}, status=400)

    strength_label, strength_percent, strength_color = calculate_strength(password, selected_types)
    crack_time = estimate_crack_time(password, selected_types)

    return JsonResponse({
        'password': password,
        'strength_label': strength_label,
        'strength_percent': strength_percent,
        'strength_color': strength_color,
        'crack_time': crack_time,
    })
