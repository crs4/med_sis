FROM node:22-alpine3.21

WORKDIR /app

COPY . .

RUN npm install
RUN npm install sharp
RUN npm run build
#RUN npm run dev

EXPOSE 3000

CMD ["npm", "start"]

