FROM node:20-alpine3.19

WORKDIR /app

# install dependencies first
COPY package*.json ./

RUN npm ci --omit=dev

# copy app source
COPY . .

# create non-root user
RUN adduser -D appuser
USER appuser

EXPOSE 3000

HEALTHCHECK CMD wget --spider http://localhost:3000/health || exit 1

CMD ["node", "app.js"]
