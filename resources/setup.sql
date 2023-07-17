CREATE TABLE "partners" (
	"id"	integer NOT NULL UNIQUE,
	"username"	varchar,
	"firstname"	varchar NOT NULL,
	"lastname"	varchar,
	"is_bot"	integer NOT NULL,
	"last_active"	datetime NOT NULL DEFAULT current_timestamp,
	PRIMARY KEY("id")
);

CREATE TABLE "users_partners" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"dt"	datetime DEFAULT current_timestamp,
	"user_vk_id"	INTEGER NOT NULL,
	"partner_vk_id"	INTEGER,
	"command"	TEXT,
	FOREIGN KEY("user_id") REFERENCES "partners"("id")
);