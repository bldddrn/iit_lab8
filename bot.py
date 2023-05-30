import telebot
import openai
from prometheus_client import start_http_server, Counter, Histogram
import time

bot_token = '6120279690:AAGNpxrremUE-sQFQV9V9_jo19LI3aY3hpM'
openai_token = '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'
openai.api_key = openai_token

bot = telebot.TeleBot(bot_token)

requests_counter = Counter('bot_requests_total', 'Total number of bot requests')
response_time_histogram = Histogram('bot_response_time_seconds', 'Bot response time in seconds')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    start_time = time.time()

    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=user_input,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )

    generated_text = response.choices[0].text.strip()


    bot.send_message(message.chat.id, generated_text)

    requests_counter.inc()

    response_time = time.time() - start_time
    response_time_histogram.observe(response_time)

def log_message(user_input, generated_text):
    pass

if __name__ == '__main__':
    start_http_server(9091)

    bot.polling()