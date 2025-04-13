FROM node:23-slim	

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY server/src/package*.json ./
RUN npm install 
RUN npm install -g typescript ts-node
RUN npm install -g nodemon

# Bundle app source
COPY server/src/ src/
COPY server/tsconfig.json ./

# build the app
RUN npm run build

COPY server/public/ public/

ENV PORT=3000
ENV NODE_ENV=production
EXPOSE 3000
RUN ["npm", "run", "start"]


