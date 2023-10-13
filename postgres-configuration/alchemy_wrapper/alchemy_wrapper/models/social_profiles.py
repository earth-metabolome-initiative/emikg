"""SQLAlchemy model for the social profiles of users."""
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from alchemy_wrapper.models.base import Base
from alchemy_wrapper.models.social import Social

class SocialProfile(Base):

    __tablename__ = "social_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    social_id = Column(Integer, ForeignKey("socials.id", ondelete="CASCADE"), nullable=False)
    url = Column(String(255), nullable=False)

    # There can be only a single social profile for a given user and social.
    __table_args__ = (UniqueConstraint("user_id", "social_id"),)


    def get_icon_path(self):
        """Return social icon path.
        
        Implementation details
        ----------------------
        We query the path to the icon of the social profile from the social
        table of the database.
        """
        return Social.from_id(self.social_id).icon_path