# GraphQL API (Strawberry)

A Python GraphQL API using Strawberry for managing books.

## Features

- Full GraphQL schema with queries and mutations
- Real-time type checking with Strawberry
- Filtering and pagination
- Search functionality
- Library statistics
- FastAPI integration for serving

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python app.py
```

The GraphQL endpoint runs on `http://localhost:8000/graphql`

## GraphQL Playground

Open `http://localhost:8000/graphql` in your browser to access the GraphQL Playground.

## GraphQL Queries

### Get All Books
```graphql
query {
  books(limit: 10, offset: 0) {
    books {
      id
      title
      author
      genre
      rating
      available
    }
    total
  }
}
```

### Get Single Book
```graphql
query {
  book(id: "1") {
    id
    title
    author
    isbn
    publishedYear
    genre
    rating
    available
  }
}
```

### Search Books
```graphql
query {
  searchBooks(query: "code") {
    id
    title
    author
  }
}
```

### Filter Books
```graphql
query {
  books(filter: { genre: "Technology", minRating: 4.0, availableOnly: true }) {
    books {
      title
      author
      rating
    }
    total
  }
}
```

### Get Genres
```graphql
query {
  genres
}
```

### Get Statistics
```graphql
query {
  stats {
    totalBooks
    totalAuthors
    averageRating
    availableCount
    genres
  }
}
```

## GraphQL Mutations

### Create Book
```graphql
mutation {
  createBook(input: {
    title: "Clean Architecture"
    author: "Robert C. Martin"
    isbn: "978-0134494326"
    publishedYear: 2017
    genre: "Technology"
    rating: 4.7
    available: true
  }) {
    id
    title
    author
  }
}
```

### Update Book
```graphql
mutation {
  updateBook(
    id: "1"
    input: {
      rating: 4.9
      available: false
    }
  ) {
    id
    title
    rating
    available
  }
}
```

### Delete Book
```graphql
mutation {
  deleteBook(id: "1") {
    success
    message
    id
  }
}
```

### Toggle Availability
```graphql
mutation {
  toggleAvailability(id: "1") {
    id
    title
    available
  }
}
```

## curl Examples

### Query (via POST)
```bash
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ books { books { title author } total } }"}'
```

### Mutation (via POST)
```bash
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { createBook(input: { title: \"Test Book\", author: \"Test Author\", isbn: \"123-456\", publishedYear: 2024, genre: \"Fiction\" }) { id title } }"
  }'
```

## Data Model

### Book
| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier (UUID) |
| title | string | Book title |
| author | string | Author name |
| isbn | string | ISBN number |
| published_year | int | Publication year |
| genre | string | Book genre |
| rating | float | Rating (0-5) |
| available | bool | Availability status |
| created_at | string | ISO timestamp |
| updated_at | string | ISO timestamp |

## Example Workflow

```bash
# Create a book
BOOK_RESPONSE=$(curl -s -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { createBook(input: { title: \"New Book\", author: \"Author\", isbn: \"999-999\", publishedYear: 2024, genre: \"Fiction\" }) { id title } }"}')

BOOK_ID=$(echo $BOOK_RESPONSE | python -c "import sys,json; print(json.load(sys.stdin)['data']['createBook']['id'])")

# Get the book
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"{ book(id: \\\"$BOOK_ID\\\") { title author } }\"}"

# Update the book
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"mutation { updateBook(id: \\\"$BOOK_ID\\\", input: { rating: 4.5 }) { title rating } }\"}"

# Delete the book
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"mutation { deleteBook(id: \\\"$BOOK_ID\\\") { success message } }\"}"
```

## License

MIT
