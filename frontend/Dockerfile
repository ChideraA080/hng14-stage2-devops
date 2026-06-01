FROM node:20-bookworm-slim

WORKDIR /app

# Install dependencies + curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

COPY package*.json ./

RUN npm ci --omit=dev && npm cache clean --force

COPY . .

RUN groupadd -r appgroup && useradd -r -g appgroup appuser
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
CMD curl -f http://localhost:3000 || exit 1

CMD ["node", "app.js"]
