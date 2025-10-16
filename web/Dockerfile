FROM node:24-alpine
WORKDIR /app

# reproduz os exatos pacotes que você acabou de resolver
COPY package.json package-lock.json ./
RUN npm ci

COPY . .

EXPOSE 3000
CMD ["npm","run","dev"]
