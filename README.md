# Lana Bot - Telegram Smart Chat Bot

## Project Overview

Lana Bot is an innovative project that combines modern DevOps practices with cutting-edge technologies. It leverages Docker, Python, APIs, and MongoDB to create a dynamic, multi-container Docker application. Each container in this system plays a unique role, working together to process and respond to data in real-time using AI and machine learning.

## Architecture

The application is structured around Docker containers, each serving a specific purpose:

- **Telegram Bot Container (`mohamedabubaker09/lana_bot`):** Hosts Python scripts (`app.py` and `bot.py`) for Telegram API interactions and integrates OpenAI API for text processing. Also, interacts with Amazon S3 for image storage and retrieval.
- **YOLOv5 Container (`mohamedabubaker09/lana_yolo5`):** Dedicated to image processing with YOLOv5, handling image detection and analysis.
- **MongoDB Containers (`mongo1`, `mongo2`, `mongo3`):** Forms a MongoDB replica set, ensuring data availability and redundancy for persistent data storage.

## Functionality

The bot is powered by Python scripts, with `app.py` managing HTTP requests and Telegram API interactions. The `bot.py` script handles message processing, coordinates with YOLOv5 and S3, and manages the overall operational flow. The YOLOv5 container processes images and communicates results back to the Telegram bot.

## DevOps Integrations

Key DevOps practices integrated into the project:

- **Docker Containerization:** Provides consistency, simplifies deployment, and isolates dependencies.
- **CI/CD:** Enables automated testing and deployment.
- **GitHub Version Control:** Facilitates collaborative development and effective change management.
- **Monitoring and Security:** Utilizes Snyk for vulnerability scanning and NGROK for secure tunneling.

## Challenges and Solutions

The project addressed challenges in container communication and data consistency through Docker networks and MongoDB's replica set, ensuring seamless operation and data integrity.

## Conclusion

Lana Bot is a testament to the practical application of DevOps, AI, and cloud services in software development. It showcases the effectiveness of Docker and Python in real-time data processing, emphasizing agility, scalability, and robustness.

