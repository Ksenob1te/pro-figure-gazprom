from typing import Optional

from sqlalchemy import JSON, PickleType, ForeignKey, Table, Column, DateTime
from uuid import uuid4, UUID
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableList
from . import Base
from typing import List
from datetime import datetime
# from config import configuration


class User(Base):
    __tablename__ = "user_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    # chat_id: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    role_id: Mapped[UUID] = mapped_column(
        ForeignKey("role_table.id"), unique=True)
    role: Mapped["Role"] = relationship(lazy="selectin")

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, email={self.email})"


class UserStats(Base):
    __tablename__ = "user_stats_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    level: Mapped[int] = mapped_column(default=1)
    experience: Mapped[int] = mapped_column(default=0)

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("user_table.id"), unique=True)
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
    date_earned: Mapped[datetime] = mapped_column(default=func.now())

    user_stats_id: Mapped[UUID] = mapped_column(
        ForeignKey("user_stats_table.id"))
    user_stats: Mapped["UserStats"] = relationship(lazy="selectin")

    achievement_id: Mapped[UUID] = mapped_column(
        ForeignKey("achievement_table.id"))
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
    permission_id: Mapped[UUID] = mapped_column(
        ForeignKey("permission_table.id"))

    role: Mapped[Role] = relationship(lazy="selectin")
    perm: Mapped[Permission] = relationship(lazy="selectin")

    def __repr__(self):
        return f"RolePerm(id={self.id}, role_id={self.role_id}, perm_id={self.permission_id})"


class File(Base):
    __tablename__ = "file_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    s3_bucket: Mapped[str]
    s3_key: Mapped[str]

    file_name: Mapped[str]

    created_date: Mapped[datetime] = mapped_column(server_default=func.now())
    last_modified_date: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now())

    public_url: Mapped[str | None] = mapped_column(nullable=True)

    owner_id: Mapped[UUID] = mapped_column(ForeignKey("user_table.id"))
    owner: Mapped[User] = relationship(lazy="selectin")


class Company(Base):
    __tablename__ = "company_table"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]

    logo_id: Mapped[UUID] = mapped_column(ForeignKey("file_table.id"))
    logo: Mapped[File] = relationship(lazy="selectin")


class HackathonDirection(Base):
    __tablename__ = "hackathon_direction_table"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]


class Hackathon(Base):
    __tablename__ = "hackathon_table"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    description: Mapped[str]

    max_solution_count: Mapped[int]
    max_team_size: Mapped[int]

    start_registration: Mapped[datetime]
    end_registration: Mapped[datetime]
    start_date: Mapped[datetime]
    end_date: Mapped[datetime]

    direction_id: Mapped[UUID] = mapped_column(
        ForeignKey("hackathon_direction_table.id"))
    direction: Mapped[HackathonDirection] = relationship(lazy="selectin")

    company_id: Mapped[UUID] = mapped_column(ForeignKey("company_table.id"))
    company: Mapped[Company] = relationship(lazy="selectin")


class HackathonFile(Base):
    __tablename__ = "hackathon_file_table"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    hackathon_id: Mapped[UUID] = mapped_column(
        ForeignKey("hackathon_table.id"))
    hackathon: Mapped[Hackathon] = relationship(lazy="selectin")

    file_id: Mapped[UUID] = mapped_column(ForeignKey("file_table.id"))
    file: Mapped[File] = relationship(lazy="selectin")


class Team(Base):
    __tablename__ = "team_table"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]

    leader_id: Mapped[UUID] = mapped_column(ForeignKey("user_table.id"))
    leader: Mapped[User] = relationship(lazy="selectin")

    hackathon_id: Mapped[UUID] = mapped_column(
        ForeignKey("hackathon_table.id"))
    hackathon: Mapped[Hackathon] = relationship(lazy="selectin")


class TeamMember(Base):
    __tablename__ = "team_member_table"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    team_id: Mapped[UUID] = mapped_column(ForeignKey("team_table.id"))
    team: Mapped[Team] = relationship(lazy="selectin")

    user_id: Mapped[UUID] = mapped_column(ForeignKey("user_table.id"))
    user: Mapped[User] = relationship(lazy="selectin")


class Solution(Base):
    __tablename__ = "solution_table"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    team_id: Mapped[UUID] = mapped_column(ForeignKey("team_table.id"))
    team: Mapped[Team] = relationship(lazy="selectin")

    status: Mapped[str]

    hackathon_id: Mapped[UUID] = mapped_column(
        ForeignKey("hackathon_table.id"))
    hackathon: Mapped[Hackathon] = relationship(lazy="selectin")


class SolutionFile(Base):
    __tablename__ = "solution_file_table"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    solution_id: Mapped[UUID] = mapped_column(ForeignKey("solution_table.id"))
    solution: Mapped[Solution] = relationship(lazy="selectin")

    file_id: Mapped[UUID] = mapped_column(ForeignKey("file_table.id"))
    file: Mapped[File] = relationship(lazy="selectin")
