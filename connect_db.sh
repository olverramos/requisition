# APP_NAME=Arvii
# DATABASE_USERNAME=admin
# DATABASE_PASSWORD=am3ricas2024
# DATABASE_NAME=requisitiondb
# DATABASE_HOST=arvii.i9iybpi.mongodb.net
# DATABASE_PORT=27017
# DATABASE_SCHEME=mongodb+srv
# DATABASE_URL="$DATABASE_SCHEME://$DATABASE_USERNAME:$DATABASE_PASSWORD@$DATABASE_HOST/$DATABASE_NAME?authSource=$DATABASE_USERNAME&appName=$APP_NAME"


mongosh "mongodb+srv://admin:am3ricas2024@arvii.i9iybpi.mongodb.net/requisitiondb?w=majority&retryWrites=true&authSource=admin&appName=Arvii"

# echo "Connecting to $DATABASE_URL..."
# mongosh $DATABASE_URL