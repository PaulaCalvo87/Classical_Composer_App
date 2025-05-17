import requests
import random

'''This program asks the user to type a classical music composer's name and creates a list with the complete name,
birth and death dates and historical period information, which is returned to the user. The information about 
the complete name, birth and death dates are stored in a .txt file. 
The user then has the opportunity to get a musical recommendation.'''

COMPOSER_FILE = 'composer.txt'

def get_composer_data(composer_name): #Gets musical composer's information and stores it in a .txt file

    composer_endpoint = f'https://api.openopus.org/composer/list/search/{composer_name}.json'
    response = requests.get(composer_endpoint)

    if response.status_code != 200:
        return "Error fetching data. Please check your internet connection or try again later."

    data = response.json()
    if not data['composers']:
        return f"No composer found for '{composer_name}'. Please check the spelling or try a different name."


    composer_info_list = [data['composers'][0]['complete_name'],
                          data['composers'][0]['birth'],
                          data['composers'][0]['death'],
                          data['composers'][0]['epoch']] #list that holds the composer's complete name, birth and death dates and historical period information

    composer_info = (
        f"\n🎼 {composer_info_list[0]}\n"
        f"📅 Born: {composer_info_list[1]}\n"
        f"🪦 Died: {composer_info_list[2]}\n"
        f"📚 Period: {composer_info_list[3]}\n"
    )


    with open(COMPOSER_FILE, 'a') as txt_file: # Opens (or creates) composer.txt in append mode and assigns the file object to txt_file
        txt_file.write('Composer information:\n')
        for info in composer_info_list[0:3]: #slicing used for exclude the 'epoch' field
            txt_file.write(f"{info}\n") #The composer's complete name, birth and death dates are written to a text file
        txt_file.write('\n')

    return composer_info

def get_music_recommendation(composer_name): #get a music recommendation
    get_recommendation = input('Would you like a music recommendation? (y/n):\n').strip().lower()

    if get_recommendation == 'y':
        composer_works_endpoint = f'https://api.openopus.org/omnisearch/{composer_name}/0.json'
        response = requests.get(composer_works_endpoint)

        if response.status_code != 200:
            return "Error retrieving musical works. Please try again later."

        data = response.json()
        valid_works = [item['work']['title'] for item in data.get('results', []) if item.get('work')]

        if not valid_works:
            return f"No musical works found for {composer_name}."

        chosen_work = random.choice(valid_works)
        return f"\n🎵 Here's a {composer_name} music recommendation:\n▶️ {chosen_work}\nEnjoy!\n"

    else:
        return "\n👍 No problem. Run the program again to explore another composer!\n"

def main():  # Main program loop: prompts the user for a composer, retrieves data, and offers a music recommendation.
    print('🎻 Welcome to the Classical Composers App! 🎶\n')

    while True:
        composer_name = input('Enter a classical composer (or type "exit" to quit):\n').strip().title()
        if composer_name.lower() == 'exit':
            print("\n👋 Enjoy. Goodbye!")
            break

        print(get_composer_data(composer_name))
        print(get_music_recommendation(composer_name))


if __name__ == "__main__":
    main()