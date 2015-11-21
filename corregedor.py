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
arquivoTweetsRespondidos = open('tweets_respondidos.txt','a+') # banco de Tweets já respondidos
tweetsRespondidos = []

for linha in arquivoTweetsRespondidos:
	tweetsRespondidos.append(linha.strip())

# Chave = palavra errada; valor = correção
dicionario = {}
arquivoDicionario = open('dicionario.txt','r')

# Lê cada linha do arquivo, separa pelo delimitador ':' e adiciona ao dicionário
for linha in arquivoDicionario:
	dicionario[linha.partition(':')[0]] = linha.partition(':')[1]
arquivoDicionario.close()

# Mensagens que mudam aleatoriamente para não deixar as respostas tão robóticas
mensagens = [u"Você sabia que o correto é ", u"Que tal ", u"Já pensou em escrever ", u"Não acha melhor ", u"Olha, já pensou em escrever ", u"Dica: sabia que o correto é ", u"Você cometeu um erro. Sabia que o certo é "]

for chave, valor in dicionario.iteritems():
	query = chave + " -RT" # Constrói a query da pesquisa, ignorando RTs
	publicTweets = api.search(query,"pt")
	# Trabalha com os 3 mais recentes Tweets encontrados
	for tweet in publicTweets[0:2]:
		# Se o Tweet já foi respondido antes, pula para o próximo
		if str(id_tweet) in tweetsRespondidos:
			print "[*] Tweet já respondido, pulando para o próximo Tweet"
			continue
		usuario = tweet.user.screen_name
		time.sleep(random.uniform(0.5, 80)) # Para o script em tempos aleatórios
		reply = "@" + usuario + " " + random.choice(mensagens) + "\"" + valor + "\"" + "?"
		# Escreve no banco de Tweets
		arquivoTweetsRespondidos.write(str(tweet.id)+"\n")
		# Envia reply
		try:
			api.update_status(reply, tweet.id)
		except:
			print "[*] Ocorreu algum erro. Pulando para o próximo Tweet"
			continue
		# Faz RT
		api.retweet(tweet.id)
		print reply

arquivoTweetsRespondidos.close()
