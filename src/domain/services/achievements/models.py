from dataclasses import dataclass

@dataclass
class AchievementRequest:
    code: str
    name: str
    description: str
    experience_reward: int = 0
    is_hidden: bool = False
