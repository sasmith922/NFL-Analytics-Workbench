# PostgreSQL Local Configuration

The local stack provisions PostgreSQL 16 through Docker Compose.

## Defaults

- Database: `nfl_analytics`
- User: `nfl_user`
- Password: `nfl_password`
- Host (containers): `postgres`
- Host (local machine): `localhost`
- Port: `5432`

Override values in the root `.env` file.
