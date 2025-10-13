DATABASE_URL="mongodb://admin:am3ricas2024@localhost:27017/communitydb?authSource=admin"

echo "Connecting to $DATABASE_URL..."
mongosh $DATABASE_URL
