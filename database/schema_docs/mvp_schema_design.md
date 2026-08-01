# MVP PostgreSQL Schema Design (Core NFL Analytics)

## Design reasoning

The MVP schema is intentionally normalized around stable entities (players, teams, seasons, games) and fact tables (player game statistics, team game statistics).

1. **Stable dimensions first**
   - `players`, `teams`, and `seasons` represent reusable dimensions referenced by many facts.
   - Keeping these separate prevents duplication across every game/stat row.

2. **Game as the event boundary**
   - `games` is the central event entity linking a season and two teams.
   - Unique constraints prevent duplicate scheduling records for the same matchup slot.

3. **Separate player and team fact tables**
   - `player_game_statistics` stores one row per player per game (per team context).
   - `team_game_statistics` stores one row per team per game.
   - This separation avoids mixing granularities and keeps aggregate/team-level analytics independent from player-level analytics.

4. **Historical integrity and analytical querying**
   - Foreign keys enforce referential integrity.
   - Check constraints prevent invalid values (for example, negative attempts or impossible week ranges).
   - Indexed foreign keys and common filter columns support typical analytics queries (season, week, player, team).

5. **MVP scope control**
   - Fantasy, betting, injuries, weather, and machine learning feature tables are intentionally excluded from this migration.
   - The schema leaves room to add those modules later without restructuring the MVP core.

## Core relationships

- `seasons 1 -> many games`
- `teams 1 -> many games` (home and away)
- `games 1 -> many player_game_statistics`
- `games 1 -> many team_game_statistics`
- `players 1 -> many player_game_statistics`
- `teams 1 -> many player_game_statistics`
- `teams 1 -> many team_game_statistics`
