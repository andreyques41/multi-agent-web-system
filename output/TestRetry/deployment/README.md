# Deployment Instructions for TestRetry

## Prerequisites
1. Docker and Docker Compose installed on the server.
2. A domain name configured to point to the server's IP address.
3. Environment variables set in a `.env` file based on `.env.example`.

## Steps to Deploy

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Set Up Environment Variables
1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Update the `.env` file with production values.

### 3. Build and Start Containers
Run the following command to build and start the application:
```bash
docker-compose up -d --build
```

### 4. Verify Deployment
Check the following:
- The web application is running at `http://<your-domain>`.
- Database health check passes using `docker-compose ps`.

### 5. Set Up CI/CD (Optional)
1. Configure GitHub Secrets for CI/CD:
   - `DOCKER_HOST`: SSH URL for the server (e.g., `ssh://username@ip-address`)
   - `DOCKER_USERNAME`: Docker Hub username
   - `DOCKER_PASSWORD`: Docker Hub password
2. Push changes to the `main` branch to trigger the CI/CD pipeline.

## Monitoring and Logs
- Use `docker-compose logs -f` to monitor logs.
- Check Nginx logs in the container for detailed HTTP request logs.

## Backup and Restore
- Backup the database using:
  ```bash
  docker exec -t <db-container-name> pg_dumpall -c -U postgres > backup.sql
  ```
- Restore the database using:
  ```bash
  cat backup.sql | docker exec -i <db-container-name> psql -U postgres
  ```

## Troubleshooting
- Check container statuses:
  ```bash
  docker-compose ps
  ```
- Restart services:
  ```bash
  docker-compose restart
  ```

For further assistance, refer to the project documentation or contact support.