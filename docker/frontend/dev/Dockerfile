FROM node:lts-alpine

WORKDIR /app

COPY frontend/package*.json ./
RUN npm set audit false
RUN npm install
