from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Boolean
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# main three tables for prediction (plant details, plant disease details and disease medicine table)


class Plant(Base):
    __tablename__ = 'plants'

    id = Column(Integer, primary_key=True, index=True)
    plant_name = Column(String(155), nullable=False)
    science_name = Column(String(155), nullable=False)
    description = Column(Text)

    disease = relationship(
        "PlantDesease",  back_populates='belong_plant')


class PlantDesease(Base):
    __tablename__ = 'plant_deseases'

    id = Column(Integer, primary_key=True, index=True)
    desease_name = Column(String(155), nullable=False)
    desease_short_description = Column(String(155), nullable=True)
    symptoms = Column(Text, nullable=True)
    description = Column(Text)
    plant_id = Column(Integer, ForeignKey(
        'plants.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)

    belong_plant = relationship(
        'Plant',  back_populates='disease')
    medicene = relationship("PlantDeseaseMedicene",
                            back_populates="plant_medicene")
    disease_image = relationship("PlantDiseaseImages",
                                 back_populates="plant_image")


class PlantDeseaseMedicene(Base):
    __tablename__ = "plant_desease_medicines"

    id = Column(Integer, primary_key=True, index=True)
    medicene_type = Column(String(155), nullable=False)
    medicene_description = Column(Text)
    disease_id = Column(Integer, ForeignKey(
        'plant_deseases.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)

    plant_medicene = relationship('PlantDesease', back_populates='medicene')

# plant_disease image model use for add images for plant diseases


class PlantDiseaseImages(Base):
    __tablename__ = "plant_disease_images"

    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(Text)
    disease_id = Column(Integer, ForeignKey(
        'plant_deseases.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=True)

    plant_image = relationship(
        'PlantDesease', back_populates='disease_image')


#!!community section
# **Admin model**
class Admin(Base):
    __tablename__ = "Admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(155), nullable=False)
    password = Column(Text, nullable=False)
    profile_picture = Column(Text)


# **USER model**
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(155), nullable=False)
    last_name = Column(String(155), nullable=False)
    username = Column(String(155), nullable=False, unique=True)
    email = Column(String(155), nullable=False, unique=True)
    phone_number = Column(String(35), nullable=False)
    location = Column(String(155), nullable=False)
    password = Column(Text, nullable=False)
    profile_picture = Column(Text)

    posts = relationship("CommunityPost", back_populates='owner')
    user_comments = relationship("Comments", back_populates='user')
    user_vote = relationship("VotePost",
                             back_populates='voteOwner')
    user_comment_vote = relationship("VoteComment",
                                     back_populates='CommentvoteOwner')


class CommunityPost(Base):
    __tablename__ = "community_posts"

    id = Column(Integer, primary_key=True, index=True)
    post_title = Column(String(155), nullable=False)
    post_date = Column(DateTime(timezone=True), default=func.now())
    description = Column(Text)
    up_vote_count = Column(Integer, default=0)
    down_vote_count = Column(Integer, default=0)
    is_approve = Column(Boolean, unique=False, default=False)
    userId = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    owner = relationship("User", back_populates='posts')
    images = relationship("CommunityPostImages",
                          back_populates='relate_image_post')
    vote = relationship("VotePost",
                        back_populates='votePost')
    comment = relationship("Comments",
                           back_populates='relate_post')


class CommunityPostImages(Base):
    __tablename__ = "community_post_images"

    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(Text)
    postId = Column(Integer, ForeignKey('community_posts.id',
                    ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    relate_image_post = relationship("CommunityPost", back_populates='images')


class Comments(Base):
    __tablename__ = "community_comments"

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(Text)
    comment_date = Column(DateTime(timezone=True), default=func.now())
    up_vote_count = Column(Integer, default=0)
    down_vote_count = Column(Integer, default=0)
    postId = Column(Integer, ForeignKey(
        'community_posts.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    userid = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    relate_post = relationship("CommunityPost", back_populates='comment')
    user = relationship("User", back_populates='user_comments')
    comment_vote = relationship("VoteComment", back_populates='voteComment')


class VotePost(Base):
    __tablename__ = "vote_posts"

    id = Column(Integer, primary_key=True, index=True)
    postId = Column(Integer, ForeignKey(
        'community_posts.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    is_up_vote = Column(Boolean, unique=False, default=False)
    is_down_vote = Column(Boolean, unique=False, default=False)
    userId = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    voteOwner = relationship("User", back_populates='user_vote')
    votePost = relationship("CommunityPost", back_populates='vote')


class VoteComment(Base):
    __tablename__ = "vote_comments"

    id = Column(Integer, primary_key=True, index=True)
    commentId = Column(Integer, ForeignKey(
        'community_comments.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    is_up_vote = Column(Boolean, unique=False, default=False)
    is_down_vote = Column(Boolean, unique=False, default=False)
    userId = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    CommentvoteOwner = relationship(
        "User", back_populates='user_comment_vote')
    voteComment = relationship(
        "Comments", back_populates='comment_vote')
