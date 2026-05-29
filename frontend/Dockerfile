# hadolint ignore=DL3018

FROM node:20-alpine3.20

WORKDIR /app

# install dependencies first (NO apk upgrade)
RUN apk add --no-cache wget

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


