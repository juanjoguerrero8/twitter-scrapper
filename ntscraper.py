import pandas as pd
from datetime import datetime
import json
import os
from ntscraper import Nitter
import time

class TwitterScraper:
    def __init__(self):
        self.tweets = []
        # Lista de instancias Nitter conocidas que suelen funcionar bien
        self.nitter_instances = [
            "nitter.net",
            "nitter.cz",
            "nitter.it",
            "nitter.pw",
            "nitter.poast.org",
            "nitter.mint.lgbt",
            "nitter.esmailelbob.xyz"
        ]
        
    def try_instances(self, username, search_term=None, limit=100):
        """
        Intenta diferentes instancias de Nitter hasta que una funcione
        """
        for instance in self.nitter_instances:
            print(f"Intentando con la instancia: {instance}")
            try:
                scraper = Nitter(instance)
                results = scraper.get_tweets(username, mode='user', number=limit)
                
                if results and 'tweets' in results and results['tweets']:
                    return results
                
            except Exception as e:
                print(f"Error con la instancia {instance}: {str(e)}")
                time.sleep(2)  # Esperar un poco antes de intentar la siguiente instancia
                continue
                
        return None
        
    def scrape_tweets(self, username, search_term=None, limit=100):
        """
        Obtiene tweets de un usuario específico
        username: Nombre de usuario sin @
        search_term: Término de búsqueda opcional para filtrar los tweets
        limit: Número máximo de tweets a recuperar
        """
        print(f"Buscando tweets del usuario @{username}")
        if search_term:
            print(f"Filtrando por el término: {search_term}")
        
        results = self.try_instances(username, search_term, limit)
        
        if not results:
            print("No se pudieron obtener tweets de ninguna instancia")
            return False
            
        try:
            for tweet in results['tweets']:
                # Si hay término de búsqueda, filtrar solo los tweets que lo contengan
                if search_term and search_term.lower() not in tweet['text'].lower():
                    continue
                    
                tweet_data = {
                    'texto': tweet['text'],
                    'fecha': tweet['date'],
                    'usuario': tweet['user']['username'],
                    'likes': tweet.get('stats', {}).get('likes', 0),
                    'retweets': tweet.get('stats', {}).get('retweets', 0),
                    'url': tweet['link']
                }
                self.tweets.append(tweet_data)
                
            print(f"Se encontraron {len(self.tweets)} tweets")
            return True
            
        except Exception as e:
            print(f"Error al procesar tweets: {str(e)}")
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

def main():
    # Crear instancia del scraper
    scraper = TwitterScraper()
    
    # Definir usuario y término de búsqueda
    username = "JonahLupton"
    search_term = "hedge"
    
    # Obtener los tweets
    scraper.scrape_tweets(username, search_term, limit=100)
    
    # Guardar los resultados
    scraper.save_results()

if __name__ == "__main__":
    main()