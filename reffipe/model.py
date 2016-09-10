# -*- coding: utf-8 -*-

import enum

from sqlalchemy import Boolean, Column, Enum, Float, ForeignKey, Integer, Table, UnicodeText, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base(object):
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()


# Enumeration of ingredient measurements
class MeasurementEnum(enum.Enum):
    cup = 'C'
    teaspoon = 'tsp'
    tablespoon = 'tbsp'
    item = 'item'


# Enumeration of time measurements
class TimeEnum(enum.Enum):
    day = 'd'
    hour = 'h'
    minute = 'm'
    second = 's'

# Association table for ingredients+recipes
recipe_ingredients = Table('recipe_ingredients', Base.metadata,
                           Column('recipe_id', ForeignKey('recipe.id'), primary_key=True),
                           Column('ingredient_id', ForeignKey('ingredient.id'), primary_key=True),
                          )

# Association table for recipes+tags
recipe_tags = Table('recipe_tags', Base.metadata,
                    Column('recipe_id', ForeignKey('recipe.id'), primary_key=True),
                    Column('tag_id', ForeignKey('tag.id'), primary_key=True),
                   )


class Step(Base):
    """One step in a recipe"""
    order = Column(Integer)
    directions = Column(UnicodeText)
    recipe_id = Column(Integer, ForeignKey('recipe.id'))


class Tag(Base):
    """A tag to ID a recipe"""
    name = Column(UnicodeText, unique=True)
    recipes = relationship('Recipe',
                           secondary=recipe_tags,
                           back_populates='tags',
                           cascade='all')


class TimeDuration(Base):
    """A length of time, such as used in meal prep"""
    time = Column(Float)
    unit = Column(Enum(TimeEnum))


class RecipeIngredient(Base):
    """One ingredient in a recipe"""
    ingredient = relationship('Ingredient', cascade='all, delete-orphan', back_populates='recipes')
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'))
    recipe = relationship('Recipe', back_populates='ingredients')
    quantity = Column(Float)
    unit = Column(Enum(MeasurementEnum))
    description = Column(UnicodeText)
    Notes = Column(UnicodeText)


class Ingredient(Base):
    """An ingredient, shared between multiple recipes"""
    name = Column(UnicodeText)
    recipes = relationship('RecipeIngredient', back_populates='ingredient')


class Recipe(Base):
    """Contains all of the data for one recipe"""
    name = Column(UnicodeText)
    ingredients = relationship('RecipeIngredient', cascade='all, delete-orphan', back_populates='recipe')
    directions = relationship('Step', cascade='all, delete-orphan')
    # prep time
    # cook time
    notes = Column(UnicodeText)
    tags = relationship('Tag',
                        secondary=recipe_tags,
                        back_populates='recipes',
                        cascade='all')
    favorite = Column(Boolean)


class MealPlanRecipe(Base):
    """A recipe as part of a meal plan"""
    order = Column(Integer)
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    recipe = relationship('Recipe')
    quantity = Column(Float)
    comment = Column(UnicodeText)
    mealplan_id = Column(Integer, ForeignKey('mealplan.id'))


class MealPlan(Base):
    """An ordered set of meal plan recipes"""
    recipes = relationship('MealPlanRecipe', cascade='all, delete-orphan')
    comments = Column(UnicodeText)


class ShoppingListRecipe(Base):
    """A recipe as part of a shopping list"""
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    recipe = relationship('Recipe')
    quantity = Column(Float)
    shoppinglist_id = Column(Integer, ForeignKey('shoppinglist.id'))


class ShoppingListIngredient(Base):
    """An entry on the to-buy list for a shopping list"""
    ingredient = relationship('Ingredient')
    ingredient_id = Column(ForeignKey('ingredient.id'))
    quantity = Column(Float)
    unit = Column(Enum(MeasurementEnum))


class ShoppingList(Base):
    """An unordered list of recipes paired with a list of ingredients"""
    name = Column(UnicodeText)
    recipes = relationship('ShoppingListRecipe', cascade='all, delete-orphan')
    ingredients = relationship('ShoppingListIngredient', cascade='all, delete-orphan')

engine = create_engine('sqlite:///reffipe.sqlite')

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
