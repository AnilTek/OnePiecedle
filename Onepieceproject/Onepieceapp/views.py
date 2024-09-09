from django.shortcuts import render, HttpResponse
import csv
import os
from django.conf import settings
import random
from django.http import JsonResponse

csv_file_path = os.path.join(settings.BASE_DIR, 'Onepieceapp', 'character_data.csv')
characters_data = {}

with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        character_name = row['name']
        characters_data[character_name] = {
            'affiliation': row['affiliation'],
            'devil_fruit': row['devil_fruit'],
            'bounty': row['bounty'],
            'height': row['height'],
            'origin': row['origin'],
            'haki': row['haki'],
            'image': row['image']
        }

is_random_selected = False
random_selected_char_list = None
users_guesses = []

does_user_guessed_correctly = False


def base(request):
    global is_random_selected, random_selected_char_list,users_guesses,does_user_guessed_correctly


 #---------------------------------------------------------------------
    suggestion_query = request.GET.get('suggestion_query')
    if suggestion_query:
        matches = [name for name in characters_data.keys() if name.lower().startswith(suggestion_query.lower())]
        return JsonResponse({'suggestions': matches})
 #---------------------------------------------------------------------




    users_char = request.GET.get('character') 
    if not users_char:  
        return render(request, 'base.html')  
    
 

    
    if users_char not in characters_data:
        return HttpResponse("Character not found")
    

    if not is_random_selected or random_selected_char_list is None:
        random_key = random.choice(list(characters_data.keys()))
        selected_character = characters_data[random_key]
        random_selected_char_list = list(selected_character.values())
        request.session['random_selected_char'] = random_selected_char_list
        is_random_selected = True
    else:
        random_selected_char_list = request.session['random_selected_char'] 
        print('Random Char already exists')
        print(random_selected_char_list)

    selected_char = characters_data[users_char]
    users_char_list = list(selected_char.values())

    def compare_chars(random_char, user_char):
        results_affiliation = random_char[0] == user_char[0]
        results_devil_fruit = random_char[1] == user_char[1]
        results_bounty = 0 if random_char[2] == user_char[2] else (1 if random_char[2] > user_char[2] else 2)
        results_height = 0 if random_char[3] == user_char[3] else (1 if random_char[3] > user_char[3] else 2)
        results_origin = random_char[4] == user_char[4]
        results_haki = random_char[5] == user_char[5]
        return [results_affiliation, results_devil_fruit, results_bounty, results_height, results_origin, results_haki]

    results_of_comp = compare_chars(random_char=random_selected_char_list, user_char=users_char_list)


    if random_selected_char_list == users_char_list : 
        is_random_selected = False
        does_user_guessed_correctly = True
        users_guesses = []


    users_guesses = [users_char_list[0],users_char_list[1],users_char_list[2],users_char_list[3],users_char_list[4],users_char_list[5]]

    print(random_selected_char_list)



    

    context = {
        'results': results_of_comp, 
        'random_character': random_selected_char_list,
        'user_character': users_char_list,
        'affiliation_correct': results_of_comp[0],
        'devil_fruit_correct': results_of_comp[1],
        'bounty_comparison': results_of_comp[2],
        'height_comparison': results_of_comp[3],
        'origin_correct': results_of_comp[4],
        'haki_correct': results_of_comp[5],
        'users_guesses':users_guesses,
        'does_user_guessed_correctly' : does_user_guessed_correctly,
    }

    return render(request, 'base.html', context)


