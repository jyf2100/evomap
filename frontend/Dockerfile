FROM node:20-slim as builder

WORKDIR /app

COPY package.json ./
RUN npm install --legacy-peer-deps --noproxy=registry.npmjs.org --proxy= --https-proxy=

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
