FROM node:12
WORKDIR /app

COPY package.json .
RUN npm install --quiet
COPY /public /app/public
COPY /src /app/src

RUN ["npm", "run", "build"]