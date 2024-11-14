import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime
import json
import os

class TwitterScraper:
    def __init__(self):
        self.tweets = []
        
    def scrape_tweets(self, query, limit=100):
        """
        Obtiene tweets basados en una consulta de búsqueda
        query: La consulta de búsqueda (ejemplo: 'from:JonahLupton hedge')
        limit: Número máximo de tweets a recuperar
        """
        print(f"Buscando tweets que coincidan con: {query}")
        
        try:
            # Realizar la búsqueda
            for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
                if i >= limit:
                    break
                    
                tweet_data = {
                    'texto': tweet.rawContent,
                    'fecha': tweet.date.strftime('%Y-%m-%d %H:%M:%S'),
                    'usuario': tweet.user.username,
                    'likes': tweet.likeCount,
                    'retweets': tweet.retweetCount,
                    'url': f"https://twitter.com/{tweet.user.username}/status/{tweet.id}"
                }
                self.tweets.append(tweet_data)
                
            print(f"Se encontraron {len(self.tweets)} tweets")
            return True
            
        except Exception as e:
            print(f"Error al obtener tweets: {str(e)}")
            return False
    
    def save_results(self, output_dir='tweet_results'):
        """
        Guarda los tweets en múltiples formatos
        """
        if not self.tweets:
            print("No hay tweets para guardar")
            return
            
        # Crear directorio si no existe
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Guardar como CSV
        df = pd.DataFrame(self.tweets)
        csv_path = os.path.join(output_dir, f'tweets_{timestamp}.csv')
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"Tweets guardados en: {csv_path}")
        
        # Guardar como JSON
        json_path = os.path.join(output_dir, f'tweets_{timestamp}.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.tweets, f, ensure_ascii=False, indent=2)
        print(f"Tweets guardados en: {json_path}")
        
        # Guardar como TXT formateado
        txt_path = os.path.join(output_dir, f'tweets_{timestamp}.txt')
        with open(txt_path, 'w', encoding='utf-8') as f:
            for tweet in self.tweets:
                f.write(f"Tweet de @{tweet['usuario']} - {tweet['fecha']}\n")
                f.write(f"{tweet['texto']}\n")
                f.write(f"URL: {tweet['url']}\n")
                f.write(f"Likes: {tweet['likes']} | Retweets: {tweet['retweets']}\n")
                f.write("-" * 80 + "\n\n")
        print(f"Tweets guardados en: {txt_path}")

# Ejemplo de uso
if __name__ == "__main__":
    # Crear instancia del scraper
    scraper = TwitterScraper()
    
    # Definir la búsqueda
    query = "from:JonahLupton hedge"
    
    # Obtener los tweets
    scraper.scrape_tweets(query, limit=100)
    
    # Guardar los resultados
    scraper.save_results()
