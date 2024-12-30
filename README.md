# Password Manager

For Users:
+----------------+--------------+------+-----+---------+----------------+
| Field          | Type         | Null | Key | Default | Extra          |
+----------------+--------------+------+-----+---------+----------------+
| id             | int          | NO   | PRI | NULL    | auto_increment |
| username       | varchar(255) | NO   | UNI | NULL    |                |
| password_hash  | varchar(255) | NO   |     | NULL    |                |
| created_at     | timestamp    | YES  |     | CURRENT_TIMESTAMP |      |
+----------------+--------------+------+-----+---------+----------------+

For Passwords:
+----------------+--------------+------+-----+---------+----------------+
| Field          | Type         | Null | Key | Default | Extra          |
+----------------+--------------+------+-----+---------+----------------+
| id             | int          | NO   | PRI | NULL    | auto_increment |
| user_id        | int          | NO   | MUL | NULL    |                |
| website_name   | varchar(255) | NO   |     | NULL    |                |
| website_url    | varchar(255) | YES  |     | NULL    |                |
| password_hash  | varchar(255) | NO   |     | NULL    |                |
| created_at     | timestamp    | YES  |     | CURRENT_TIMESTAMP |      |
+----------------+--------------+------+-----+---------+----------------+
