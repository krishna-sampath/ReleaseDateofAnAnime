from telegram.ext import *
import requests
TOKEN = '5956397925:AAEhq87te_klDaPP5k4wj2KjyXAe8YurWss'

def run_my_python_code(name):
    def get_anime_id(name):
    # Set the API endpoint URL and the search query
        URL = "https://graphql.anilist.co"
        QUERY = name

        # Set the API headers
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Set the API query
        query = """
        query ($query: String) {
        Media (search: $query, type: ANIME) {
            id
            title {
            romaji
            }
        }
        }
        """

        # Set the API variables
        variables = {
            "query": QUERY
        }

        # Set the API request body
        data = {
            "query": query,
            "variables": variables
        }

        # Make a POST request to the API
        response = requests.post(URL, json=data, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            # Parse the response data
            data = response.json()

            # Get the ID of the anime
            anime_id = data["data"]["Media"]["id"]
        else:
            # There was an error making the request
            anime_id = None

        return anime_id
    def get_start_data(ANIME_Id):
        URL = "https://graphql.anilist.co"
        ANIME_ID = ANIME_Id

        # Set the API headers
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Set the API query
        query = """
        query ($id: Int) {
            Media (id: $id) {
            startDate {
                year
                month
                day
            }
            }
        }
        """

        # Set the API variables
        variables = {
            "id": ANIME_ID
        }

        # Set the API request body
        data = {
            "query": query,
            "variables": variables
        }

        # Make a POST request to the API
        response = requests.post(URL, json=data, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            # Parse the response data
            data = response.json()

            # Get the start date of the anime
            start_date = data["data"]["Media"]["startDate"]
            year = start_date["year"]
            month = start_date["month"]
            day = start_date["day"]

            # Format the start date as a string
            release_date = f"{day}-{month}-{year}"
        else:
            # There was an error making the request
            release_date = None
        return release_date
    a_id = get_anime_id(name)
    rd = get_start_data(a_id)
    return rd
def start_command(update, context):
    update.message.reply_text('Hello There! You have started the bot')
def help_command(update, context):
    update.message.reply_text('type \\custom to start the bot and then enter the anime of your liking')
def custom_command(update, context):
    update.message.reply_text('Now please enter the anime of your liking')
def handle_response(txt: str)->str:
    return run_my_python_code(txt)
def handle_message(update, context):
    message_type = update.message.chat.type
    txt = str(update.message.text)
    response = ''

    print('User ({update.message.chat.id}) says: "{txt} in {message.type}"')
    if message_type == 'group':
        if'https://t.me/JamesRathriBot' in txt:
            new_text = txt.replace('https://t.me/JamesRathriBot', '').strip()
            response = handle_response(new_text)
    else:
        response = handle_response(txt)
    
    update.message.reply_text('Release Date of the anime '+txt+' is '+response)
def error(update,context):
    print(f'Update {update} caused error: {context.error}')
if __name__ == "__main__":
    updater = Updater(TOKEN, use_context=True)
    #Commands
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('custom', custom_command))
    #Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    #Errors
    dp.add_error_handler(error)
    #Running the Bot

    updater.start_polling(1.0)
    updater.idle()