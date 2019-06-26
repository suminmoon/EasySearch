token = '636670076:AAFgJ7kM8IIqbZVQnQeIUdw2UkX3H5gWjZs'
api_url = f'https://api.telegram.org/bot{token}'
webhook_url = input()
print(f'{api_url}/setWebhook?url={webhook_url}/pages/telegram_bot/')

