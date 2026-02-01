# Meeting Room Reservation API

This is a technical assessment project featuring a simple REST API for booking meeting rooms. The application is built with **Python** and **FastAPI**, and is fully containerized using **Docker**.

## Features
* **Create Reservations:** Includes overlap checks and prevents bookings in the past.
* **Cancel Reservations:** Delete bookings using a unique ID.
* **View Reservations:** List all bookings filtered by room.
* **Validation:** Comprehensive input validation (e.g., timezone-aware datetime handling and string length constraints).

## Getting Started (Docker)

The fastest way to run the application is using Docker Compose:

1. Ensure Docker is installed and running.
2. Run the following command in the project root:
   ```bash
   docker-compose up --build
