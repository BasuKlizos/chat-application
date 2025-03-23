# FROM node:22-alpine

# WORKDIR /app
    
# COPY package.json package-lock.json ./

# RUN npm install --only=production

# COPY . .

# EXPOSE 3000

# CMD ["npm", "start"]

# Use a smaller base image
FROM node:22-alpine

# Set work directory
WORKDIR /app

# Copy package files first for better caching
COPY package.json package-lock.json ./

# Install dependencies (production only)
RUN npm ci --only=production

# Copy the remaining files
COPY . .

# Avoid running as root for security
USER node

# Expose the port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
