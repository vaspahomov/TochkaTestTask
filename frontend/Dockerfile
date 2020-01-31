FROM node:12
WORKDIR /app

COPY package.json .
RUN npm install --quiet
COPY . .
CMD ["npm", "run", "build"]