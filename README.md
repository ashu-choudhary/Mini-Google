

# 🔍 Mini-Google: A Distributed Search Engine

This project is a small-scale, distributed web search engine built from the ground up. It demonstrates core concepts in distributed systems, information retrieval, and web crawling. The goal is to create a scalable system that can crawl web pages, index their content, and serve search queries with ranked results, similar to how major search engines operate.

---

## 🚀 Features

- **Distributed Crawler**: Multiple crawler instances can run in parallel to fetch web pages.
- **Scalable Indexer**: A dedicated service to process and index web content.
- **Inverted Index**: Uses Elasticsearch to build and manage a powerful inverted index for fast lookups.
- **Ranking**: Leverages Elasticsearch's built-in BM25 algorithm for relevance ranking.
- **Query Service**: A simple API to handle user search queries.
- **Containerized**: The entire application stack is managed with Docker and Docker Compose for easy setup and deployment.

---

## 🧱 System Architecture

The system is designed using a microservices architecture, where each component is a separate, independently scalable service.

```
                              +-----------------+
                        +---->|   Crawler #1    |-----+
                        |     +-----------------+     |
                        |                             |
+-----------------+     |     +-----------------+     |
|      User       |---->|   Query Service (API + Cache)  |<----> Elasticsearch (Inverted Index)
+-----------------+     +-----------------+     |
                        |     Redis (Queue + Cache)      |
                        +-----------------+              |
                        |     +-----------------+        |
                        +---->|   Crawler #2    |--------+
                              +-----------------+
```

### Components

1. **Crawler (`crawler-service`)**  
   Discovers and downloads web pages. It uses Redis as a shared queue for URLs to crawl.

2. **Indexer (`indexer-service`)**  
   Receives text content from the crawlers, processes it, and stores it in Elasticsearch.

3. **Query Service (`query-service`)**  
   Exposes a public API for users to submit search queries. It queries Elasticsearch and returns ranked results.

4. **Redis**  
   Acts as a message broker (URL queue) for the crawlers and a cache for the query service.

5. **Elasticsearch**  
   The core search and analytics engine. It stores all the indexed web page data and provides powerful full-text search capabilities.

---

## 🛠 Tech Stack

- **Backend**: Python
- **Web Framework**: Flask / FastAPI
- **Data Stores**:
  - Elasticsearch (for indexing and searching)
  - Redis (for queuing and caching)
- **Containerization**: Docker & Docker Compose
- **Libraries**:
  - `requests`
  - `beautifulsoup4`
  - `redis-py`
  - `elasticsearch-py`

---

## ⚙️ Getting Started

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.8+](https://www.python.org/downloads/)

---

## 🚀 Running the Application

1. **Clone the repository**  
   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>
   ```

2. **Start the infrastructure (Redis & Elasticsearch)**  
   This command will download the necessary images and start the containers in the background:
   ```bash
   docker-compose up
   ```

3. **Run the services**  
   In separate terminal windows, navigate to the project directory and run each service:

   - Run the Crawler:
     ```bash
     python crawler-service/crawler.py
     ```

   - (Coming Soon) Run the Indexer:
     ```bash
     python indexer-service/indexer.py
     ```

   - (Coming Soon) Run the Query Service:
     ```bash
     python query-service/app.py
     ```

---

## 📁 Project Structure

```
.
├── crawler-service/
│   └── crawler.py
├── indexer-service/
│   └── indexer.py
├── query-service/
│   └── app.py
├── docker-compose.yml
└── README.md
```

---

## 📄 License

This project is intended for educational and learning purposes.

---

## 🙋‍♂️ Contact

For any suggestions, issues, or collaboration, please feel free to open an issue or submit a pull request on GitHub.
