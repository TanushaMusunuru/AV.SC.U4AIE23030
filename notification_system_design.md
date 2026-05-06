# Stage 1

## Notification System Overview

This system is used to send notifications to students for:

- Placements
- Results
- Events

The system supports:
- Sending notifications
- Viewing notifications
- Marking notifications as read
- Real-time notification updates

---

## 1. Send Notification API

### Endpoint

POST /notifications

### Headers

```json
{
  "Authorization": "Bearer <token>",
  "Content-Type": "application/json"
}
```

### Request Body

```json
{
  "studentId": 1042,
  "type": "Placement",
  "message": "Afford Medical Technologies"
}
```

### Response

```json
{
  "success": true,
  "message": "Notification sent successfully"
}
```

---

## 2. Get Notifications API

### Endpoint

GET /notifications/{studentId}

### Headers

```json
{
  "Authorization": "Bearer <token>"
}
```

### Response

```json
{
  "notifications": [
    {
      "id": "N101",
      "type": "Placement",
      "message": "Afford Medical Technologies",
      "isRead": false
    }
  ]
}
```

---

## 3. Mark Notification as Read API

### Endpoint

PUT /notifications/{notificationId}/read

### Headers

```json
{
  "Authorization": "Bearer <token>"
}
```

### Response

```json
{
  "success": true,
  "message": "Notification marked as read"
}
```

---

## Notification Schema

| Field | Type |
|---|---|
| id | String |
| studentId | Integer |
| type | String |
| message | String |
| isRead | Boolean |

---

## Real-Time Notification Mechanism

WebSockets can be used for real-time notifications.

### Flow

1. Student connects to server
2. Backend sends notification instantly
3. Frontend receives updates without refresh

### Benefits

- Faster delivery
- Real-time updates
- Better user experience

---

# Stage 2

## Database Choice

I would use PostgreSQL for storing notifications because it is reliable and works well for structured data. It also supports indexing and handles large amounts of data efficiently.

---

## Notification Table Schema

| Column | Type |
|---|---|
| id | VARCHAR |
| studentId | INTEGER |
| type | VARCHAR |
| message | TEXT |
| isRead | BOOLEAN |
| createdAt | TIMESTAMP |

---

## SQL Table

```sql
CREATE TABLE notifications (
    id VARCHAR(50) PRIMARY KEY,
    studentId INTEGER,
    type VARCHAR(20),
    message TEXT,
    isRead BOOLEAN DEFAULT false,
    createdAt TIMESTAMP
);
```

---

## Possible Problems as Data Increases

- Query performance may become slow
- More storage will be required
- Fetching unread notifications may take longer
- Database load may increase

---

## Solutions

- Add indexes on commonly searched fields
- Use pagination while fetching notifications
- Archive older notifications
- Optimize queries

---

## Queries

### Insert Notification

```sql
INSERT INTO notifications
(id, studentId, type, message, isRead, createdAt)
VALUES
('N101', 1042, 'Placement',
'Afford Medical Technologies',
false, NOW());
```

### Get Notifications

```sql
SELECT * FROM notifications
WHERE studentId = 1042
ORDER BY createdAt DESC;
```

### Get Unread Notifications

```sql
SELECT * FROM notifications
WHERE studentId = 1042
AND isRead = false;
```

### Mark Notification as Read

```sql
UPDATE notifications
SET isRead = true
WHERE id = 'N101';
```

---

# Stage 3

## Given Query

```sql
SELECT * FROM notifications
WHERE studentID = 1042
AND isRead = false
ORDER BY createdAt DESC;
```

---

## Is the Query Correct?

Yes, the query is correct because it fetches unread notifications of a student and sorts them by latest notifications first.

---

## Why Is It Slow?

The query may become slow because the database now contains millions of notifications. Without proper indexing, the database may scan many rows before returning results.

---

## Improvements

Indexes can be added on:

- studentId
- isRead
- createdAt

Example:

```sql
CREATE INDEX idx_notifications
ON notifications(studentId, isRead, createdAt DESC);
```

This helps improve filtering and sorting speed.

---

## Should We Add Indexes on Every Column?

No.

Adding indexes on every column is not a good approach because:

- It increases storage usage
- Insert and update operations become slower
- Some indexes may never be used

Indexes should only be added for frequently searched columns.

---

## Query for Placement Notifications in Last 7 Days

```sql
SELECT * FROM notifications
WHERE type = 'Placement'
AND createdAt >= NOW() - INTERVAL '7 days';
```


# Stage 4

## Problem

Notifications are fetched every time the page loads for every student. As the number of users increases, the database receives too many requests which affects performance and user experience.

---

## Solutions

### 1. Pagination

Instead of loading all notifications at once, load only a limited number of notifications.

Example:
- Load first 10 notifications
- Load more when user scrolls

#### Benefits

- Reduces database load
- Faster response time
- Better user experience

#### Tradeoff

- User needs multiple requests to view older notifications

---

### 2. Caching

Frequently accessed notifications can be temporarily stored in cache using Redis.

#### Benefits

- Faster data access
- Reduces repeated database queries

#### Tradeoff

- Extra memory usage
- Cache needs periodic updates

---

### 3. Fetch Only Unread Notifications

Instead of fetching every notification, fetch only unread notifications initially.

#### Benefits

- Less data transfer
- Faster API response

#### Tradeoff

- Older read notifications require separate fetch requests

---

### 4. Real-Time Updates Using WebSockets

Instead of requesting notifications repeatedly, use WebSockets to push new notifications instantly.

#### Benefits

- Reduces unnecessary API calls
- Real-time updates
- Better user experience

#### Tradeoff

- More complex implementation
- Requires persistent connections

---

## Final Approach

A combination of:
- Pagination
- Caching
- WebSockets

would provide better scalability and improved performance for large-scale notification systems.


# Stage 5

## Problems in Current Implementation

The current implementation has some issues:

- Sending emails one by one is slow
- If email sending fails midway, some students may not receive notifications
- Database and email operations are tightly connected
- System performance may decrease for 50,000 students
- Failure recovery is difficult

---

## What Happens if Email Fails for 200 Students?

If the process fails midway:

- Some students receive notifications
- Some students do not receive notifications
- System becomes inconsistent

Retry handling is needed for failed notifications.

---

## Improved Design

The process can be improved using queues and background workers.

Steps:
1. Save notification to database first
2. Add email task to queue
3. Background worker sends emails
4. Retry failed email tasks

This makes the system faster and more reliable.

---

## Should DB Save and Email Sending Happen Together?

No.

Saving to DB and sending emails should happen separately.

Reason:
- Database operations are fast
- Email APIs can be slow or fail
- Separating them improves reliability

---

## Improved Pseudocode

```python
function notify_all(student_ids, message):

    for student_id in student_ids:

        save_to_db(student_id, message)

        add_to_email_queue(student_id, message)

        push_to_app(student_id, message)
```

---

## Retry Mechanism

If email sending fails:

- Failed tasks can be retried automatically
- Retry count can be maintained
- Logs can be stored for monitoring

---

## Benefits of Improved Design

- Faster processing
- Better scalability
- Reliable notification delivery
- Easier failure recovery
- Reduced system load

# Stage 6

## Priority Inbox System

A priority inbox system is used to display the most important unread notifications first.

Priority is decided using:

- Notification type
- Notification recency

Priority order:

- Placement
- Result
- Event

Recent notifications are given higher importance.

---

## Approach

1. Fetch notifications from API
2. Assign weight based on notification type
3. Combine weight and timestamp
4. Sort notifications by priority
5. Display top 10 notifications

---

## Efficient Maintenance of Top Notifications

Instead of sorting the complete notification list repeatedly, a priority queue or heap can be used to maintain the top notifications efficiently when new notifications arrive.

This reduces processing time and improves performance.