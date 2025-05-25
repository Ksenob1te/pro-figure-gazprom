from typing import Optional

from sqlalchemy import JSON, PickleType, ForeignKey, Table, Column, DateTime
from uuid import uuid4, UUID
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableList
from . import Base
from typing import List
import datetime
# from config import configuration


class User(Base):
    __tablename__ = "user_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    #chat_id: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    role_id: Mapped[UUID] = mapped_column(ForeignKey("role_table.id"), unique=True)
    role: Mapped["Role"] = relationship(lazy="selectin")

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, email={self.email})"


class UserStats(Base):
    __tablename__ = "user_stats_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    level: Mapped[int] = mapped_column(default=1)
    experience: Mapped[int] = mapped_column(default=0)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user_table.id"), unique=True)
    user: Mapped["User"] = relationship(lazy="selectin")

    def __repr__(self) -> str:
        return (f"UserStats(id={self.id}, level={self.level}, experience={self.experience}, "
                f"user_id={self.user_id})")


class Achievement(Base):
    __tablename__ = "achievement_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    description: Mapped[str]
    experience_reward: Mapped[int] = mapped_column(default=0)
    is_hidden: Mapped[bool] = mapped_column(default=False)


    def __repr__(self) -> str:
            return f"Achievement(id={self.id}, code={self.code}, name={self.name})"


class UserAchievement(Base):
    __tablename__ = "user_achievement"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    date_earned: Mapped[datetime.datetime] = mapped_column(default=func.now())

    user_stats_id: Mapped[UUID] = mapped_column(ForeignKey("user_stats_table.id"))
    user_stats: Mapped["UserStats"] = relationship(lazy="selectin")

    achievement_id: Mapped[UUID] = mapped_column(ForeignKey("achievement_table.id"))
    achievement: Mapped["Achievement"] = relationship(lazy="selectin")

    def __repr__(self) -> str:
        return (f"UserAchievement(id={self.id}, date_earned={self.date_earned}, "
                f"user_stats_id={self.user_stats_id}, achievement_id={self.achievement_id})")




class Permission(Base):
    __tablename__ = "permission_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(unique=True)

    def __repr__(self) -> str:
        return f"Permission(id={self.id}, name={self.name})"


class Role(Base):
    __tablename__ = "role_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(unique=True)

    def __repr__(self) -> str:
        return f"Role(id={self.id}, name={self.name})"
#
#
class RolePerm(Base):
    __tablename__ = "role_perm_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    role_id: Mapped[UUID] = mapped_column(ForeignKey("role_table.id"))
    permission_id: Mapped[UUID] = mapped_column(ForeignKey("permission_table.id"))

    role: Mapped[Role] = relationship(lazy="selectin")
    perm: Mapped[Permission] = relationship(lazy="selectin")

    def __repr__(self):
        return f"RolePerm(id={self.id}, role_id={self.role_id}, perm_id={self.permission_id})"

#
# class League(Base):
#     __tablename__ = "league_table"
#
#     id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
#     league_id: Mapped[int] = mapped_column(unique=True)
#     league_type: Mapped[str]
#     league_name: Mapped[str] = mapped_column(nullable=False)
#     league_data: Mapped[JSON] = mapped_column(type_=JSON, nullable=True, default={})
#
#     def __repr__(self) -> str:
#         return f"League(id={self.id}, league_id={self.league_id}, league_type={self.league_type})"
#
#
# class Team(Base):
#     __tablename__ = "team_table"
#
#     id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
#     entry: Mapped[int] = mapped_column(nullable=True, unique=True)
#     name: Mapped[str] = mapped_column()
#     leader: Mapped[str] = mapped_column()
#     pts_total: Mapped[int] = mapped_column()
#     pts_gw: Mapped[int] = mapped_column()
#     players_played: Mapped[int] = mapped_column(nullable=True)
#     pick: Mapped[dict] = mapped_column(type_=JSON, nullable=True, default={})
#
#     def __repr__(self):
#         return f"Team(id={self.id}, entry={self.entry}, name={self.name}, leader={self.leader})"
#
#
# class UserLeague(Base):
#     __tablename__ = "user_league_table"
#
#     id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
#
#     user_id: Mapped[UUID] = mapped_column(ForeignKey("user_table.id"))
#     league_id: Mapped[UUID] = mapped_column(ForeignKey("league_table.id"))
#
#     user: Mapped[User] = relationship(lazy="selectin")
#     league: Mapped[League] = relationship(lazy="selectin")
#
#     def __repr__(self):
#         return f"UserLeague(user_id={self.user_id}, league_id={self.league_id})"
#
#
# class UserTeam(Base):
#     __tablename__ = "user_team_table"
#
#     id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
#
#     user_id: Mapped[UUID] = mapped_column(ForeignKey("user_table.id"))
#     team_id: Mapped[UUID] = mapped_column(ForeignKey("team_table.id"))
#
#     user: Mapped[User] = relationship(lazy="selectin")
#     team: Mapped[Team] = relationship(lazy="selectin")
#
#     def __repr__(self):
#         return f"UserTeam(user_id={self.user_id}, team_id={self.team_id})"
#
#
# class UserGoat(Base):
#     __tablename__ = "user_goat_table"
#
#     id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
#
#     user_id: Mapped[UUID] = mapped_column(ForeignKey("user_table.id"))
#     user: Mapped[User] = relationship(lazy="selectin")
#
#     name: Mapped[str] = mapped_column()
#     update_type: Mapped[int] = mapped_column(nullable=False, default=2)
#
#     goats: Mapped[int] = mapped_column(default=0)
#     points: Mapped[int] = mapped_column(default=0)
#     participated: Mapped[int] = mapped_column(default=0)
#     money_amount: Mapped[int] = mapped_column(default=0)
#
#     def __repr__(self):
#         return f"UserGoat(user_id={self.user_id}, name={self.name})"
#
#
# class Gameweek(Base):
#     __tablename__ = "gameweek_table"
#
#     id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
#
#     gameweek: Mapped[int] = mapped_column(unique=True)
#     is_current: Mapped[bool] = mapped_column(default=False)
#     weekly_started: Mapped[bool] = mapped_column(default=False)
#     weekly_finished: Mapped[bool] = mapped_column(default=False)
#     intergame_started: Mapped[bool] = mapped_column(default=False)
#     intergame_finished: Mapped[bool] = mapped_column(default=False)
#
#     deadline: Mapped[datetime.datetime] = mapped_column(nullable=False)
#     notifications: Mapped[List[int]] = mapped_column(MutableList.as_mutable(PickleType), default=[])
#
#     def __repr__(self):
#         return f"Gameweek(id={self.id}, gameweek={self.gameweek})"
#
#
# class GoatGameweek(Base):
#     __tablename__ = "goat_gameweek_table"
#
#     id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
#
#     gameweek_id: Mapped[UUID] = mapped_column(ForeignKey("gameweek_table.id"))
#     gameweek: Mapped[Gameweek] = relationship(lazy="selectin")
#
#     subs_open: Mapped[datetime.datetime] = mapped_column(nullable=False)
#     deadline: Mapped[datetime.datetime] = mapped_column(nullable=False)
#     finish: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None)
#
#     open_notification: Mapped[bool] = mapped_column(default=False)
#     draft_notifications: Mapped[List[int]] = mapped_column(MutableList.as_mutable(PickleType), default=[])
#     leaderboards_update: Mapped[bool] = mapped_column(default=False)
#     bots_countdown: Mapped[int] = mapped_column(default=configuration.goat.bots_addition)
#
#     def __repr__(self) -> str:
#         return (f"GoatGameweek(id={self.id}, gameweek={self.gameweek}, subs_open={self.subs_open},"
#                 f" deadline={self.deadline}, finish={self.finish})")
#
#
# class GoatPick(Base):
#     __tablename__ = "goat_pick_table"
#
#     id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
#
#     user_goat_id: Mapped[UUID] = mapped_column(ForeignKey("user_goat_table.id"))
#     user_goat: Mapped[UserGoat] = relationship(lazy="selectin")
#
#     goat_gameweek_id: Mapped[UUID] = mapped_column(ForeignKey("goat_gameweek_table.id"))
#     goat_gameweek: Mapped[GoatGameweek] = relationship(lazy="selectin")
#
#     bps: Mapped[int] = mapped_column(default=0)
#     pick: Mapped[List[int]] = mapped_column(MutableList.as_mutable(PickleType), default=[])
#     submitted: Mapped[bool] = mapped_column(default=False)
#
#     def __repr__(self) -> str:
#         return (f"GoatPick(id={self.id}, user_goat={self.user_goat}, goat_gameweek={self.goat_gameweek},"
#                 f" bps={self.bps}, pick={self.pick}, submitted={self.submitted})")
#
#
# class Players(Base):
#     __tablename__ = "players_table"
#
#     id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
#
#     static_id: Mapped[int] = mapped_column(unique=True)
#     name: Mapped[str] = mapped_column()
#     real_name: Mapped[str] = mapped_column(default="")
#     points: Mapped[int] = mapped_column()
#     team: Mapped[str] = mapped_column(default="")
#     position: Mapped[int] = mapped_column(default=0)
#     price: Mapped[int] = mapped_column(default=0)
#     played: Mapped[bool] = mapped_column(default=False)
#     status: Mapped[int] = mapped_column(nullable=True, default=None)
#     news: Mapped[str] = mapped_column(default="")
#     photo: Mapped[str] = mapped_column(default="")
#
#     def __repr__(self) -> str:
#         return f"Players(id={self.id}, static_id={self.static_id}, name={self.name}"
#
#
# class UserTeamExpansion(Base):
#     __tablename__ = "user_team_expansion_table"
#
#     id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
#
#     user_team_id: Mapped[UUID] = mapped_column(ForeignKey("user_team_table.id"))
#     user_team: Mapped[UserTeam] = relationship(lazy="selectin")
#
#     league_id: Mapped[UUID] = mapped_column(ForeignKey("league_table.id"))
#     league: Mapped[League] = relationship(lazy="selectin")
#
#     def __repr__(self):
#         return f"UserTrackerExpansion(user_id={self.user_team_id}, league_id={self.league_id})"
#
#
# class LeagueExtendedExpansion(Base):
#     __tablename__ = "league_extended_expansion_table"
#
#     id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
#
#     league_id: Mapped[UUID] = mapped_column(ForeignKey("league_table.id"))
#     league: Mapped[League] = relationship(lazy="selectin")
#
#     team_id: Mapped[UUID] = mapped_column(ForeignKey("team_table.id"))
#     team: Mapped[Team] = relationship(lazy="selectin")
#
#     place: Mapped[int] = mapped_column()
#
#     def __repr__(self):
#         return f"ExtendedLeagueExpansion(league_id={self.league_id}, team_id={self.team_id}, place={self.place})"
#
#
# class LeagueH2HExpansion(Base):
#     __tablename__ = "league_h2h_expansion_table"
#
#     id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
#
#     league_id: Mapped[UUID] = mapped_column(ForeignKey("league_table.id"))
#     league: Mapped[League] = relationship(lazy="selectin")
#
#     team_id: Mapped[UUID] = mapped_column(ForeignKey("team_table.id"))
#     team: Mapped[Team] = relationship(lazy="selectin")
#
#     wins: Mapped[int] = mapped_column()
#     draws: Mapped[int] = mapped_column()
#     losses: Mapped[int] = mapped_column()
#
#     def __repr__(self):
#         return f"LeagueH2HExpansion(league_id={self.league_id}, team_id={self.team_id})"
#
#
# class UserReminder(Base):
#     __tablename__ = "user_reminder_gameweek_table"
#
#     user_id: Mapped[UUID] = mapped_column(ForeignKey("user_table.id"), primary_key=True)
#     user: Mapped[User] = relationship(lazy="selectin")
#
#     notification_times: Mapped[List[int]] = mapped_column(MutableList.as_mutable(PickleType), default=[])
#
#     def __repr__(self):
#         return f"UserReminderGameweek(user_id={self.user_id}, notification_times={self.notification_times})"
#
#
# class TeamAchievement(Base):
#     __tablename__ = "team_achievement_table"
#
#     id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
#
#     league_id: Mapped[UUID] = mapped_column(ForeignKey("league_table.id"))
#     league: Mapped[League] = relationship(lazy="selectin")
#
#     team_id: Mapped[UUID] = mapped_column(ForeignKey("team_table.id"))
#     team: Mapped[Team] = relationship(lazy="selectin")
#
#     gameweek_id: Mapped[UUID] = mapped_column(ForeignKey("gameweek_table.id"))
#     gameweek: Mapped[Gameweek] = relationship(lazy="selectin")
#
#     icon: Mapped[str] = mapped_column()
#
#     def __repr__(self):
#         return f"TeamAchievement(league_id={self.league_id}, team_id={self.team_id}, gameweek_id={self.gameweek_id})"
#
#
# class Match(Base):
#     __tablename__ = "match_table"
#
#     id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
#
#     match_id: Mapped[int] = mapped_column(unique=True)
#     gameweek_id: Mapped[UUID] = mapped_column(ForeignKey("gameweek_table.id"))
#     gameweek: Mapped[Gameweek] = relationship(lazy="selectin")
#
#     finished: Mapped[bool] = mapped_column(default=False)
#     finished_provisional: Mapped[bool] = mapped_column(default=False)
#
#     kickoff_time: Mapped[datetime.datetime] = mapped_column(nullable=True, default=None)
#     first_team: Mapped[str] = mapped_column(default="")
#     second_team: Mapped[str] = mapped_column(default="")
#
#     def __repr__(self):
#         return f"Match(id={self.id}, match_id={self.match_id}, gameweek={self.gameweek})"
#
#
# class MatchBPS(Base):
#     __tablename__ = "match_bps_table"
#
#     id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
#
#     match_id: Mapped[UUID] = mapped_column(ForeignKey("match_table.id"))
#     match: Mapped[Match] = relationship(lazy="selectin")
#
#     player_id: Mapped[UUID] = mapped_column(ForeignKey("players_table.id"))
#     player: Mapped[Players] = relationship(lazy="selectin")
#
#     bps: Mapped[int] = mapped_column(default=0)
#     minutes: Mapped[int] = mapped_column(default=0)
#
#     def __repr__(self):
#         return f"MatchBPS(match={self.match}, player={self.player}, bps={self.bps}, minutes={self.minutes})"
#
#
# class GoatBoost(Base):
#     __tablename__ = "goat_boost_table"
#
#     id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
#
#     goat_pick_id: Mapped[UUID] = mapped_column(ForeignKey("goat_pick_table.id"))
#     goat_pick: Mapped[GoatPick] = relationship(lazy="selectin")
#
#     boost_tag: Mapped[str] = mapped_column(nullable=True, default=None)
#     match_id: Mapped[int]
#
#     def __repr__(self):
#         return f"GoatBoost(id={self.id}, goat_pick={self.goat_pick}, boost_tag={self.boost_tag})"
