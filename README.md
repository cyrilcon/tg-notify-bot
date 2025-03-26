# Telegram Notification Bot

## Navigation

- [Application Description](#application-description)
- [System Architecture](#system-architecture)
- [Environment Configuration](#environment-configuration)
- [Token Generation Algorithm](#token-generation-algorithm)
- [Database Structure](#database-structure)
- [API](#API)
- [Application Testing](#application-testing)
- [Running the Application with Docker](#running-the-application-with-docker)

## Application Description

This Telegram bot provides an API for sending automated notifications via HTTP.

It is designed for integration into existing services, enabling real-time alerts about critical events like server
errors, with support for file attachments such as log files.

### Application Features:

- Interaction with the bot through the API.
- Ability to send attached files.
- Ensures secure interaction between the server and the bot using an authorization token.

### Technologies Used:

- **FastAPI**: Web framework for API creation.
- **Aiogram**: Library for asynchronous interaction with [Telegram Bot API](https://core.telegram.org/bots/api).
- **SQLAlchemy**: ORM for working with the database.
- **Alembic**: Tool for managing database migrations.
- **Pytest**: Framework for writing and running tests.
- **Docker**: Tool for containerizing the application.
- **UV**: Tool for dependency and package management.

## System Architecture

![System Architecture](images/system_architecture.png)

## Environment Configuration

| Parameter           | Description                                                                            | Default value                                    |
|---------------------|----------------------------------------------------------------------------------------|--------------------------------------------------|
| `API__ACCESS_TOKEN` | Access token for API interaction.                                                      | **Required**                                     |
| `API__RUN__HOST`    | Host on which the API will run. If running in a container, specify the container name. | `tg-notify-bot` (Docker container name)          |
| `API__RUN__PORT`    | Port on which the API will be available.                                               | `8000`                                           |
| `API__RUN__RELOAD`  | Server auto-reload flag (`1` – enabled, `0` – disabled).                               | `0`                                              |
| `DB__HOST`          | Database host. If PostgreSQL is running in a container, specify the container name.    | `tg-notify-bot-postgres` (Docker container name) |
| `DB__PORT`          | Port for connecting to the PostgreSQL database.                                        | `5432`                                           |
| `DB__USER`          | Database username.                                                                     | `postgres`                                       |
| `DB__PASSWORD`      | Database user password.                                                                | `postgres`                                       |
| `DB__DATABASE`      | Name of the database used by the application.                                          | `notification`                                   |
| `DB__ECHO`          | SQL query logging (`1` – enabled, `0` – disabled).                                     | `0`                                              |
| `DB__ECHO_POOL`     | Connection pool logging (`1` – enabled, `0` – disabled).                               | `0`                                              |
| `DB__POOL_SIZE`     | Maximum number of connections in the database pool.                                    | `50`                                             |
| `DB__MAX_OVERFLOW`  | Maximum number of additional connections created when the pool is overloaded.          | `10`                                             |
| `TG_BOT__TOKEN`     | Telegram bot token used for sending notifications.                                     | **Required**                                     |
| `TEST_CHAT_ID`      | Chat ID used for test notifications.                                                   | **Required**                                     |

> [!WARNING]\
> Before starting the application, create a `.env` file and specify all required variables.

## Token Generation Algorithm

The authentication token is generated using the **HMAC-SHA256** algorithm, where the key is `API__ACCESS_TOKEN` from
`.env`.

### **Algorithm:**

1. Retrieve configuration parameters.
2. Generate a Unix timestamp.
3. Generate an HMAC hash using SHA-256 based on `API__ACCESS_TOKEN` and the current time.

### **Token Generation Code:**

```python
import hashlib
import hmac
import time

from config import config


def generate_token() -> str:
    current_time = str(int(time.time()))
    return hmac.new(
        config.api.access_token.encode(),
        current_time.encode(),
        hashlib.sha256,
    ).hexdigest()
```

## Database Structure

The application uses PostgreSQL and includes two main tables: `Notification` and `Document`, related by a
_"one-to-many"_ relationship.

### **Table `Notification`**

| Field        | Type                     | Description                    |
|--------------|--------------------------|--------------------------------|
| `id`         | integer                  | Unique notification identifier |
| `chat_id`    | bigint                   | Chat or channel ID             |
| `message`    | text                     | Message text                   |
| `created_at` | timestamp with time zone | Notification send time         |

**ORM Model:**

```python
class Notification(Base, TableNameMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(BIGINT, index=True)
    message: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        index=True,
    )

    documents: Mapped[List["Document"]] = relationship(
        back_populates="notification",
        cascade="all, delete-orphan",
        lazy="joined",
    )
```

### **Table `Document`**

| Field             | Type    | Description                       |
|-------------------|---------|-----------------------------------|
| `id`              | integer | Unique document identifier        |
| `notification_id` | integer | ID of the associated notification |
| `buffer`          | bytea   | Byte buffer of the document       |
| `name`            | text    | File name                         |

**ORM Model:**

```python
class Document(Base, TableNameMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    notification_id: Mapped[int] = mapped_column(
        ForeignKey("notification.id", ondelete="CASCADE"),
    )
    buffer: Mapped[bytes] = mapped_column(LargeBinary)
    name: Mapped[str] = mapped_column(Text(), index=True)

    notification: Mapped["Notification"] = relationship(
        back_populates="documents",
    )
```

## API

### **Notify**

```
POST /api/v1/notify
```

- **Method:** `POST`
- **Endpoint:** `/api/v1/notify`
- **Description:** Sends a message with the ability to attach documents.

### **Request Headers:**

| Header        | Type   | Description |
|---------------|--------|-------------|
| Authorization | string | API key     |

### **Request Parameters:**

| Field       | Type    | Description                                       |
|-------------|---------|---------------------------------------------------|
| `chatID`    | integer | Chat or channel ID where the message will be sent |
| `message`   | string  | Message text in Markdown formatting               |
| `documents` | array   | *Optional*. List of attached documents            |

**Description of `document` object:**

| Field    | Type   | Description           |
|----------|--------|-----------------------|
| `buffer` | string | File in Base64 format |
| `name`   | string | Document name         |

### **Example Request:**

```json
{
  "chatID": 123456789,
  "message": "Hello, this is a message with *markdown* formatting.",
  "documents": [
    {
      "buffer": "SGVsbG8gd29ybGQ=",
      "name": "Document 1.pdf"
    },
    {
      "buffer": "U29tZSBuZXcgZGF0YQ==",
      "name": "Document 2.pdf"
    }
  ]
}
```

### **Response:**

| Field          | Type    | Description                                     |
|----------------|---------|-------------------------------------------------|
| `success`      | boolean | `true` if the message was sent successfully     |
| `errorMessage` | string  | Error message or `null` if successful           |
| `createdAt`    | string  | Time of notification sending in ISO 8601 format |

**Example Successful Response:**

```json
{
  "success": true,
  "errorMessage": null,
  "createdAt": "2024-06-06T12:00:02Z"
}
```

**Example Error Response:**

```json
{
  "success": false,
  "errorMessage": "Error message explaining what went wrong",
  "createdAt": "2024-06-06T12:00:02Z"
}
```

### **Possible Response Codes:**

| Code                        | Description               |
|-----------------------------|---------------------------|
| `201 Created`               | Message successfully sent |
| `403 Forbidden`             | Invalid token             |
| `422 Unprocessable Entity`  | Invalid data format       |
| `500 Internal Server Error` | Server error              |

## Application Testing

The project uses the **pytest** library for testing.

During test execution, the Telegram bot will send two test messages. The first time, only a markdown-formatted message
is sent, without any attached documents. The second time, the same message is sent but with an attached file
`document.txt`.

### **Running Tests:**

```sh
pytest
```

> [!WARNING]\
> Ensure that `TG_BOT__TOKEN` and `TEST_CHAT_ID` parameters are specified in the `.env` file.

### **Tested Scenarios:**

- Successful message sending:
    - Text message without attachments.
    - Text message with an attachment.
- Errors in sending:
    - Sending without a token.
    - Sending with an invalid token.
    - Sending without `chatID`.
    - Sending without `message`.
    - Sending with an incorrect `chatID`.

## Running the Application with Docker

1. Navigate to the project root directory.

2. Configure `.env`.

> [!NOTE]\
> Each `.env` parameter is described in the [environment configuration](#environment-configuration) section.

3. Build and start the containers:

   ```sh
   docker compose up --build -d
   ```