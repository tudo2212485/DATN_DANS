"""Entry point for verified historical observations (no synthetic price generation)."""
from ml_pipeline.observation_scraper import scrape_and_update_db

if __name__ == "__main__":
    print(scrape_and_update_db())
