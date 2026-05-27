FROM node:20-alpine

WORKDIR /app

# security updates (IMPORTANT for Trivy)
RUN apk update && apk upgrade

# install dependencies first
COPY package*.json ./

RUN npm ci --omit=dev

# copy app source
COPY . .

# create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

USER appuser

EXPOSE 3000

HEALTHCHECK CMD wget --spider -q http://localhost:3000/health || exit 1

CMD ["node", "app.js"]
