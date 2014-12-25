# -*- coding: utf8 -*-
import tweepy, random, time

# Preencher estas informações de acordo com as disponibilizadas pelo apps.twitter.com
CONSUMER_KEY = 'xxx'
CONSUMER_SECRET = 'xxx'

ACCESS_TOKEN = 'xxx'
ACCESS_TOKEN_SECRET = 'xxx'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
f = open('tweets_respondidos','a+') # banco de Tweets já respondidos
tweets_respondidos = [line.strip() for line in open('tweets_respondidos')] # Carrega os IDs em uma lista

# Chave = palavra errada; valor = correção
dicionario = {
				"poblema":"problema",
				"adolecente":"adolescente",
				"ploblema":"problema",
				"concerteza":"com certeza",
				"encomoda":"incomoda",
				"jente":"gente",
				"presizo":"preciso",
				"concegui":"consegui",
				"revoutado":"revoltado"
			}
# Mensagens que mudam aleatoriamente para não deixar as respostas tão robóticas
mensagens = [u"Você sabia que o correto é ", u"Que tal ",u"Já pensou em escrever ",u"Não acha melhor ",u"Olha, já pensou em escrever ", "Dica: sabia que o correto é ", "Você cometeu um erro. Sabia que o certo é "]

try:
	for chave, valor in dicionario.iteritems():
		query = chave + " -RT" # Constrói a query da pesquisa, ignorando RTs
		public_tweets = api.search(query,"pt")
		# Trabalha com os 3 mais recentes Tweets encontrados
		for tweet in public_tweets[0:3]:
			id_tweet = tweet.id
			# Se o Tweet já foi respondido antes, pula para o próximo
			if str(id_tweet) in tweets_respondidos:
				print "Tweet já respondido, pulando para o próximo"
				continue
			usuario = tweet.user.screen_name
			time.sleep(random.uniform(0.26, 4.79)) # Para o script em tempos aleatórios
			reply = "@" + usuario + " " + random.choice(mensagens) + "\"" + valor + "\"" + "?"
			# Escreve no banco de Tweets
			f.write(str(id_tweet)+"\n")
			# Envia reply
			api.update_status(reply,id_tweet)
			# Faz RT
			api.retweet(id_tweet)
			print reply
except TweepError:
	print "Erro com a API do Twitter :("
f.close()