from sqlalchemy import Column, String, Integer
from linebot.models import *
from database import Base, db_session
from urllib.parse import quote
from config import Config


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    description = Column(String)
    product_image_url = Column(String)

    @staticmethod
    def list_all():
        products = db_session.query(Products).all()

        bubbles = []

        for product in products:
            bubble = BubbleContainer(
                hero=ImageComponent(
                    size='full',
                    aspect_ratio='20:13',
                    aspect_mode='cover',
                    url=product.product_image_url
                ),
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(text=product.name,
                                      wrap=True,
                                      weight='bold',
                                      size='xl'),
                        BoxComponent(
                            layout='baseline',
                            contents=[
                                TextComponent(text='NT${price}'.format(price=product.price),
                                              wrap=True,
                                              weight='bold',
                                              size='xl')
                            ]
                        ),
                        TextComponent(margin='md',
                                      text='{des}'.format(des=product.description or ''),
                                      wrap=True,
                                      size='xs',
                                      color='#aaaaaa')
                    ],
                ),
                footer=BoxComponent(
                    layout='vertical',
                    spacing='sm',
                    contents=[
                        ButtonComponent(
                            style='primary',
                            color='#1DB446',
                            action=URIAction(label='Add to Cart',
                                             uri='line://oaMessage/{base_id}/?{message}'.format(base_id=Config.BASE_ID,
                                                                                                message=quote("{product}, I'd like to have:".format(product=product.name)))),
                        )
                    ]
                )
            )

            bubbles.append(bubble)

        carousel_container = CarouselContainer(contents=bubbles)

        message = FlexSendMessage(alt_text='products', contents=carousel_container)

        return message

