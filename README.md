### Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/storlay/online_library.git
   cd online_library
   ```

2. **Set up environment variables:**
   - Create a `.env` file in the project's root directory. You will need to populate it with the required configuration
   values (e.g., database credentials, secret keys).
   - Create public (`public.pem`) and private (`private.pem`) jwt certs in the `src/certs/jwt` directory.

3. **Build and run the application:**
   ```bash
   docker compose -f infra/docker-compose.local.yml up --build -d
   ```

4. **Access the application:**

   The API will be running and available at `http://127.0.0.1:8000`.

## Usage

### API Documentation

The API documentation is automatically generated and can be accessed at the following endpoints:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`