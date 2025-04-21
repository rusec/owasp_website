FROM node:22-alpine AS builder

# Create app directory
WORKDIR /app

# Install app dependencies
COPY package*.json ./
RUN npm install 
RUN npm install -g typescript ts-node

COPY ./src/app ./src/app
COPY ./public ./public
COPY ./next.config.ts ./
COPY ./tsconfig.json ./
COPY ./next-env.d.ts ./
COPY ./package.json ./
COPY ./eslint.config.mjs ./
COPY ./postcss.config.mjs ./

# build the app
RUN npm run build
RUN ls -l /app/build

FROM python:alpine AS runner

# Create app directory
WORKDIR /usr/src/owasp

COPY --from=builder /app/build /usr/src/frontend
COPY --from=builder /app/public /usr/src/frontend/public

RUN cp -r /usr/src/frontend /usr/src/owasp/static

COPY src/server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/server .

CMD [ "python" , "app.py", "--host=0.0.0.0", "--port=3000" ]


