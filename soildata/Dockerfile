FROM node:lts-alpine3.22

WORKDIR /app

COPY . .

RUN npm install
RUN npm install sharp
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]

