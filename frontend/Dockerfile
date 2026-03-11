# 1. Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
# If using pnpm or yarn, change this accordingly

# Install dependencies
RUN npm install

# Copy all source code
COPY . .

# Build the app with environment variable
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN echo "Building app with API URL: VITE_API_URL"
RUN npm run build

# 2. Production stage
FROM nginx:alpine

# Copy built files from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx config if needed
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Run nginx
CMD ["nginx", "-g", "daemon off;"]