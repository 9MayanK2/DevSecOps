# -----------------------------------------------------------------------------
# Base Image
# Use the official Node.js 22 Alpine image.
# Alpine Linux is lightweight, resulting in a smaller image and fewer packages.
# -----------------------------------------------------------------------------
FROM node:22-alpine

# -----------------------------------------------------------------------------
# Working Directory
# Creates (if it doesn't exist) and switches to /app.
# All following instructions (COPY, RUN, CMD, etc.) execute relative to /app.
# -----------------------------------------------------------------------------
WORKDIR /app

# -----------------------------------------------------------------------------
# Copy Dependency Files
# Copy package.json and package-lock.json first.
# This improves Docker layer caching because dependency installation only
# reruns when these files change.
# -----------------------------------------------------------------------------
COPY package*.json ./

# -----------------------------------------------------------------------------
# Install Production Dependencies
# npm ci:
#   - Uses package-lock.json exactly.
#   - Faster and more predictable than npm install.
#
# --omit=dev:
#   - Installs only production dependencies.
#   - Skips development packages like nodemon and eslint.
# -----------------------------------------------------------------------------
RUN npm ci --omit=dev

# -----------------------------------------------------------------------------
# Copy Application Source Code
# Copies controllers/, routes/, models/, middleware/, utils/, index.js, etc.
#
# Docker first checks .dockerignore and skips ignored files such as:
#   node_modules
#   .git
#   .env
# -----------------------------------------------------------------------------
COPY . .

# -----------------------------------------------------------------------------
# Documentation
# Tells anyone reading the image that this application listens on port 5000.
# EXPOSE does NOT publish the port.
# -----------------------------------------------------------------------------
EXPOSE 5000

# -----------------------------------------------------------------------------
# Default Command
# Starts the Express server when a container is created.
#
# Equivalent to:
# node index.js
#
# (Your package.json should have:
# "start": "node index.js")
# -----------------------------------------------------------------------------
CMD ["npm", "start"]
