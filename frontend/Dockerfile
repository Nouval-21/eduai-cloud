# Stage 1: Build React app
FROM node:20-alpine AS build

WORKDIR /app

# Install dependencies dulu (di-cache)
COPY package*.json .
RUN npm ci

# Copy source code dan build
COPY . .
RUN npm run build
# Hasil build ada di /app/dist

# Stage 2: Serve dengan Nginx (ringan)
FROM nginx:alpine

# Copy hasil build ke Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Copy konfigurasi Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]