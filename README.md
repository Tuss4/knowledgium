Knowledgium API Documentation
===========

Vokal hack day stuff.

## Coders (users)

### Create A New Coder

**POST:** `/api/coder/register/`

**Body:**
```json
{
    "email": "hibiki@kamenrider.co.jp",
    "password": "henshin",
    "first_name": "KR",
    "last_name": "Hibiki"
}
```

**Notes:**
- `first_name` and `last_name` are not required.

**Response:**
```json
{
    "id": 1,
    "token": "sahfdlhsafh02373274027402742128hsdfg8s83"
}
```

**Status Codes:**
- `201` if successfully created
- `400` if incorrect data is provided (badly formatted email or empty string for password)
- `409` if a Coder with this email already exists.

### Login Coder

**POST:** `/api/coder/login/`

**Body:**
```json
{
    "email": "hibiki@kamenrider.co.jp",
    "password": "henshin"
}
```

**Response:**
```json
{
    "id": 1,
    "token": "sahfdlhsafh02373274027402742128hsdfg8s83"
}
```

**Status Codes:**
- `200` if successfully logged in
- `400` if bad data were provided
- `401` if credentials are invalid

### Current Coder

**GET:** `/api/coder/`

**Body:**
```json
{
    "id": 1,
    "email": "hibiki@kamenrider.co.jp",
    "first_name": "KR",
    "last_name": "Hibiki",
    "created": "YYYY-MM-DD"
}
```

**Notes:**
- the `HTTP_AUTHORIZATION` header will have to be set to the user's token in the request
- ex: `Token sahfdlhsafh02373274027402742128hsdfg8s83` in the header

**Status Codes:**
- `200` if successful
- `401` if unauthorized
