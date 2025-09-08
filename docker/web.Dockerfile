FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install || yarn install
COPY . .
CMD ["npm", "run", "dev"]
