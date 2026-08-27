import argparse
import json
import os
import sys
import tweepy
from dotenv import load_dotenv

load_dotenv()
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

if not BEARER_TOKEN:
  print('ERRO: BEARER_TOKEN não encontrado no arquivo .env!')
  sys.exit(1)


class TwitterStream(tweepy.StreamingClient):

  def on_connect(self):
    print('✅ Conectado à Stream do X/Twitter em tempo real!\n')

  def on_tweet(self, tweet):
    try:
      tweet_data = {'id': tweet.id, 'text': tweet.text}
      print(f'🟢 Novo tweet capturado [ID: {tweet.id}]')
      print(f'   Texto: {tweet.text[:80]}...\n')

      with open('python.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(tweet_data, ensure_ascii=False) + '\n')

    except Exception as e:
      print(f'❌ Erro ao processar tweet: {e}')

  def on_errors(self, errors):
    print(f'❌ Erro na Stream: {errors}')


def run_search(hashtag, max_results=10):
  print(f"🔍 Buscando tweets recentes para: '{hashtag}'...\n")
  client = tweepy.Client(bearer_token=BEARER_TOKEN)
  query = f'{hashtag} -is:retweet'

  try:
    response = client.search_recent_tweets(
        query=query,
        tweet_fields=['created_at', 'author_id', 'lang', 'public_metrics'],
        max_results=max_results,
    )

    if response.data:
      for tweet in response.data:
        print(f'ID: {tweet.id}')
        print(f'Data: {tweet.created_at}')
        print(f'Texto: {tweet.text}')
        print('-' * 40)
    else:
      print('Nenhum tweet encontrado.')

  except Exception as e:
    print(f'❌ Erro na busca: {e}')


def run_stream(hashtag):
  print(f"📡 Iniciando escuta em tempo real para: '{hashtag}'...\n")
  stream = TwitterStream(bearer_token=BEARER_TOKEN)

  rules = stream.get_rules()
  if rules.data:
    rule_ids = [rule.id for rule in rules.data]
    stream.delete_rules(rule_ids)

  stream.add_rules(tweepy.StreamRule(hashtag))
  stream.filter(tweet_fields=['created_at', 'author_id'])


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
      description='Coletor de Dados do Twitter/X via API v2 (Tweepy)'
  )
  parser.add_argument(
      '--mode',
      choices=['search', 'stream'],
      required=True,
      help="Modo de execução: 'search' ou 'stream'",
  )
  parser.add_argument(
      '--tag',
      type=str,
      default='#python',
      help='Hashtag ou palavra-chave (Padrão: #python)',
  )

  args = parser.parse_args()

  if args.mode == 'search':
    run_search(hashtag=args.tag)
  elif args.mode == 'stream':
    run_stream(hashtag=args.tag)
