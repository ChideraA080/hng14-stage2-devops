FROM node:20-bookworm-slim

WORKDIR /app

# Install required OS tools
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends wget curl && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency files first
COPY package*.json ./

# Install dependencies
RUN npm ci --omit=dev

# Copy application source
COPY . .

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Fix permissions for node app
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 3000

# Safer healthcheck
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
CMD curl -f http://localhost:3000 || exit 1

CMD ["node", "app.js"]
