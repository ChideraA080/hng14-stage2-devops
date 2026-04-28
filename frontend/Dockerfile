FROM node:18-alpine

WORKDIR /app

# install dependencies
COPY package*.json ./
RUN npm install --only=production

# copy app
COPY . .

# create non-root user
RUN adduser -D appuser
USER appuser

EXPOSE 3000

# healthcheck
HEALTHCHECK CMD wget --spider http://localhost:3000/health || exit 1

CMD ["node", "app.js"]
