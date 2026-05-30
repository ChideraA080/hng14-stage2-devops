FROM node:20-alpine3.21

WORKDIR /app

# Install only required OS tools (NO upgrade)
RUN apk add --no-cache wget curl

# Copy dependency files first
COPY package*.json ./

# Install dependencies (production only)
RUN npm ci --omit=dev

# Copy application source
COPY . .

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

USER appuser

EXPOSE 3000

# Safer healthcheck (more stable in CI)
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
CMD curl -f http://localhost:3000/health || exit 1

CMD ["node", "app.js"]
