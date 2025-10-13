APP_NAME=Arvii
DATABASE_USERNAME=admin
DATABASE_PASSWORD=am3ricas2024
DATABASE_NAME=communitydb
DATABASE_HOST=arvii.i9iybpi.mongodb.net
DATABASE_PORT=27017
DATABASE_SCHEME=mongodb+srv
MONGO_OPTIONS="authSource=${DATABASE_USERNAME}&appName=${APP_NAME}"
DATABASE_URL=${DATABASE_SCHEME}://${DATABASE_USERNAME}:${DATABASE_PASSWORD}@${DATABASE_HOST}/${DATABASE_NAME}?${MONGO_OPTIONS}
echo ${DATABASE_URL}

heroku config:set APP_NAME=Arvii
heroku config:set ENVIRONMENT=PRODUCTION
heroku config:set DEBUG=FALSE
heroku config:set SENDGRID_API_KEY=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
heroku config:set DJANGO_SECRET_KEY=r91LtqSbgJL8s_HbI7kW2DfT9tkgTkGefvfj2_6NNk1B8Lb0A6BpdhdSQZswAslGuNGv_gezykUpi8m20RGRkw
heroku config:set DATABASE_URL=${DATABASE_URL}
heroku config:set DATABASE_NAME=${DATABASE_NAME}
heroku config:set EMAIL_HOST_USER=admin@arvii.com.co
heroku config:set EMAIL_HOST_PASSWORD=odroztabyagkpztz