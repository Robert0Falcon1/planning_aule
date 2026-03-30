# Frontend Dockerfile - ICE Planning Aule
# Vue 3 + Vite build, Nginx serve

# Stage 1: Build
FROM node:20-alpine AS build

WORKDIR /app

# Copia package files
COPY package*.json ./

# Installa dipendenze
RUN npm ci

# Copia sorgenti
COPY . .

# Variabile ambiente per API URL (iniettata a build time)
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL

# Build production
RUN npm run build

# Stage 2: Serve con Nginx
FROM nginx:1.25-alpine

# Copia configurazione nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Copia build da stage precedente
COPY --from=build /app/dist /usr/share/nginx/html

# Esponi porta
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

CMD ["nginx", "-g", "daemon off;"]
