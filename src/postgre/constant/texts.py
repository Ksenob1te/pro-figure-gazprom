from src.database import sessionmanager
from src.database import TextRepository, TextCodesEnum
from sqlalchemy.exc import IntegrityError
import logging

_default_texts = {
    TextCodesEnum.STARTER: 'Hello! Press "Send news!" to get started',
    TextCodesEnum.SUPPORT_GLOBAL_1: 'Select what publication you want to send recommendations for using buttons below!',
    TextCodesEnum.SUPPORT_GLOBAL_2: 'Send your suggestion, note that is should consists only with text, photos and videos and only one message will be selected',
    TextCodesEnum.FINAL_TEXT: 'Thanks for your submission! This message was forwarded to the admins',
    TextCodesEnum.TIMEOUT_TEXT: f"You can't suggest so soon. Timeout is 60 seconds."
}

async def create_texts():
    logger = logging.getLogger(__name__)
    async with sessionmanager.session() as session:
        text_repo = TextRepository(session)
        for text in TextCodesEnum:
            try:
                await text_repo.create(text, text=_default_texts.get(text, None))
                logger.info(f"Text {text} initialized")
            except IntegrityError:
                await session.rollback()
                logger.info(f"Text {text} already exists")
        await session.commit()



