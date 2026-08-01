"""create mvp nfl analytics schema

Revision ID: 20260801_0001
Revises:
Create Date: 2026-08-01 00:00:00.000000

"""

from __future__ import annotations

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "20260801_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "players",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("external_id", sa.String(length=64), nullable=True),
        sa.Column("first_name", sa.String(length=64), nullable=False),
        sa.Column("last_name", sa.String(length=64), nullable=False),
        sa.Column("display_name", sa.String(length=128), nullable=False),
        sa.Column("position", sa.String(length=8), nullable=True),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_players")),
        sa.UniqueConstraint("external_id", name=op.f("uq_players_external_id")),
    )
    op.create_index(op.f("ix_players_display_name"), "players", ["display_name"], unique=False)
    op.create_index(op.f("ix_players_external_id"), "players", ["external_id"], unique=False)
    op.create_index(op.f("ix_players_position"), "players", ["position"], unique=False)

    op.create_table(
        "seasons",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("year", sa.SmallInteger(), nullable=False),
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("year <= 2100", name=op.f("ck_seasons_season_year_max_2100")),
        sa.CheckConstraint("year >= 1920", name=op.f("ck_seasons_season_year_min_1920")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_seasons")),
        sa.UniqueConstraint("year", name=op.f("uq_seasons_year")),
    )
    op.create_index(op.f("ix_seasons_year"), "seasons", ["year"], unique=False)

    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("abbreviation", sa.String(length=3), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("city", sa.String(length=64), nullable=False),
        sa.Column("conference", sa.String(length=8), nullable=True),
        sa.Column("division", sa.String(length=16), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_teams")),
        sa.UniqueConstraint("abbreviation", name=op.f("uq_teams_abbreviation")),
    )
    op.create_index(op.f("ix_teams_abbreviation"), "teams", ["abbreviation"], unique=False)

    op.create_table(
        "games",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("external_id", sa.String(length=64), nullable=True),
        sa.Column("season_id", sa.Integer(), nullable=False),
        sa.Column("week", sa.Integer(), nullable=False),
        sa.Column("game_type", sa.String(length=16), nullable=False),
        sa.Column("kickoff_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("home_team_id", sa.Integer(), nullable=False),
        sa.Column("away_team_id", sa.Integer(), nullable=False),
        sa.Column("home_score", sa.Integer(), nullable=True),
        sa.Column("away_score", sa.Integer(), nullable=True),
        sa.Column("venue", sa.String(length=128), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "away_team_id <> home_team_id", name=op.f("ck_games_game_teams_must_differ")
        ),
        sa.CheckConstraint("week <= 25", name=op.f("ck_games_game_week_max_25")),
        sa.CheckConstraint("week >= 1", name=op.f("ck_games_game_week_min_1")),
        sa.ForeignKeyConstraint(
            ["away_team_id"], ["teams.id"], name=op.f("fk_games_away_team_id_teams")
        ),
        sa.ForeignKeyConstraint(
            ["home_team_id"], ["teams.id"], name=op.f("fk_games_home_team_id_teams")
        ),
        sa.ForeignKeyConstraint(
            ["season_id"], ["seasons.id"], name=op.f("fk_games_season_id_seasons")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_games")),
        sa.UniqueConstraint("external_id", name=op.f("uq_games_external_id")),
        sa.UniqueConstraint(
            "season_id", "week", "home_team_id", "away_team_id", name="uq_game_slot"
        ),
    )
    op.create_index(op.f("ix_games_away_team_id"), "games", ["away_team_id"], unique=False)
    op.create_index(op.f("ix_games_external_id"), "games", ["external_id"], unique=False)
    op.create_index(op.f("ix_games_home_team_id"), "games", ["home_team_id"], unique=False)
    op.create_index(op.f("ix_games_kickoff_at"), "games", ["kickoff_at"], unique=False)
    op.create_index(op.f("ix_games_season_id"), "games", ["season_id"], unique=False)
    op.create_index(op.f("ix_games_week"), "games", ["week"], unique=False)

    op.create_table(
        "player_game_statistics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.Column("player_id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("opponent_team_id", sa.Integer(), nullable=False),
        sa.Column("passing_attempts", sa.Integer(), nullable=False),
        sa.Column("passing_completions", sa.Integer(), nullable=False),
        sa.Column("passing_yards", sa.Integer(), nullable=False),
        sa.Column("passing_touchdowns", sa.Integer(), nullable=False),
        sa.Column("interceptions_thrown", sa.Integer(), nullable=False),
        sa.Column("rushing_attempts", sa.Integer(), nullable=False),
        sa.Column("rushing_yards", sa.Integer(), nullable=False),
        sa.Column("rushing_touchdowns", sa.Integer(), nullable=False),
        sa.Column("targets", sa.Integer(), nullable=False),
        sa.Column("receptions", sa.Integer(), nullable=False),
        sa.Column("receiving_yards", sa.Integer(), nullable=False),
        sa.Column("receiving_touchdowns", sa.Integer(), nullable=False),
        sa.Column("sacks", sa.Integer(), nullable=False),
        sa.Column("tackles", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "passing_attempts >= 0",
            name=op.f("ck_player_game_statistics_player_stats_passing_attempts_non_negative"),
        ),
        sa.CheckConstraint(
            "receptions >= 0",
            name=op.f("ck_player_game_statistics_player_stats_receptions_non_negative"),
        ),
        sa.CheckConstraint(
            "rushing_attempts >= 0",
            name=op.f("ck_player_game_statistics_player_stats_rushing_attempts_non_negative"),
        ),
        sa.ForeignKeyConstraint(
            ["game_id"], ["games.id"], name=op.f("fk_player_game_statistics_game_id_games")
        ),
        sa.ForeignKeyConstraint(
            ["opponent_team_id"],
            ["teams.id"],
            name=op.f("fk_player_game_statistics_opponent_team_id_teams"),
        ),
        sa.ForeignKeyConstraint(
            ["player_id"], ["players.id"], name=op.f("fk_player_game_statistics_player_id_players")
        ),
        sa.ForeignKeyConstraint(
            ["team_id"], ["teams.id"], name=op.f("fk_player_game_statistics_team_id_teams")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_player_game_statistics")),
        sa.UniqueConstraint(
            "game_id", "player_id", "team_id", name="uq_player_game_statistics_game_player_team"
        ),
    )
    op.create_index(
        op.f("ix_player_game_statistics_game_id"),
        "player_game_statistics",
        ["game_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_player_game_statistics_opponent_team_id"),
        "player_game_statistics",
        ["opponent_team_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_player_game_statistics_player_id"),
        "player_game_statistics",
        ["player_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_player_game_statistics_team_id"),
        "player_game_statistics",
        ["team_id"],
        unique=False,
    )

    op.create_table(
        "team_game_statistics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("points", sa.Integer(), nullable=False),
        sa.Column("first_downs", sa.Integer(), nullable=False),
        sa.Column("total_yards", sa.Integer(), nullable=False),
        sa.Column("passing_yards", sa.Integer(), nullable=False),
        sa.Column("rushing_yards", sa.Integer(), nullable=False),
        sa.Column("turnovers", sa.Integer(), nullable=False),
        sa.Column("penalties", sa.Integer(), nullable=False),
        sa.Column("penalty_yards", sa.Integer(), nullable=False),
        sa.Column("time_of_possession_seconds", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "points >= 0", name=op.f("ck_team_game_statistics_team_stats_points_non_negative")
        ),
        sa.ForeignKeyConstraint(
            ["game_id"], ["games.id"], name=op.f("fk_team_game_statistics_game_id_games")
        ),
        sa.ForeignKeyConstraint(
            ["team_id"], ["teams.id"], name=op.f("fk_team_game_statistics_team_id_teams")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_team_game_statistics")),
        sa.UniqueConstraint("game_id", "team_id", name="uq_team_game_statistics_game_team"),
    )
    op.create_index(
        op.f("ix_team_game_statistics_game_id"), "team_game_statistics", ["game_id"], unique=False
    )
    op.create_index(
        op.f("ix_team_game_statistics_team_id"), "team_game_statistics", ["team_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_team_game_statistics_team_id"), table_name="team_game_statistics")
    op.drop_index(op.f("ix_team_game_statistics_game_id"), table_name="team_game_statistics")
    op.drop_table("team_game_statistics")

    op.drop_index(op.f("ix_player_game_statistics_team_id"), table_name="player_game_statistics")
    op.drop_index(op.f("ix_player_game_statistics_player_id"), table_name="player_game_statistics")
    op.drop_index(
        op.f("ix_player_game_statistics_opponent_team_id"), table_name="player_game_statistics"
    )
    op.drop_index(op.f("ix_player_game_statistics_game_id"), table_name="player_game_statistics")
    op.drop_table("player_game_statistics")

    op.drop_index(op.f("ix_games_week"), table_name="games")
    op.drop_index(op.f("ix_games_season_id"), table_name="games")
    op.drop_index(op.f("ix_games_kickoff_at"), table_name="games")
    op.drop_index(op.f("ix_games_home_team_id"), table_name="games")
    op.drop_index(op.f("ix_games_external_id"), table_name="games")
    op.drop_index(op.f("ix_games_away_team_id"), table_name="games")
    op.drop_table("games")

    op.drop_index(op.f("ix_teams_abbreviation"), table_name="teams")
    op.drop_table("teams")

    op.drop_index(op.f("ix_seasons_year"), table_name="seasons")
    op.drop_table("seasons")

    op.drop_index(op.f("ix_players_position"), table_name="players")
    op.drop_index(op.f("ix_players_external_id"), table_name="players")
    op.drop_index(op.f("ix_players_display_name"), table_name="players")
    op.drop_table("players")
