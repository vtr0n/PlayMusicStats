FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm set audit false
RUN npm install
COPY . .
RUN npm run build

FROM nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY --from=build-stage /app/config/nginx.conf /etc/nginx/nginx.conf
#   cat /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
