from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    Message,
    ActionFailed,
    MessageSegment,
)
from nonebot.params import CommandArg
from nonebot.log import logger
from ..matcher import arc
from ..data import UserInfo
from ..draw_image import UserArcaeaInfo


async def recent_handler(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args: list = str(args).split()
    if args[0] == "recent":
        user_info = UserInfo.get_or_none(UserInfo.user_qq == event.user_id)
        if not user_info:
            try:
                await arc.finish(
                    "\n".join(
                        [f"> {event.sender.card or event.sender.nickname}", "你还没绑定哦~"]
                    )
                )
            except ActionFailed as e:
                logger.exception(
                    f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}'
                )
                return
        if not UserArcaeaInfo.is_querying(arcaea_id=user_info.arcaea_id):
            result = await UserArcaeaInfo.draw_recent_image(
                arcaea_id=user_info.arcaea_id
            )
            try:
                await arc.finish(MessageSegment.reply(event.message_id) + result)
            except ActionFailed as e:
                logger.exception(
                    f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}'
                )
                return
        else:
            try:
                await arc.finish(
                    "\n".join(
                        [
                            f"> {event.sender.card or event.sender.nickname}",
                            "您已在查询队列, 请勿重复发起查询。",
                        ]
                    )
                )
            except ActionFailed as e:
                logger.exception(
                    f'ActionFailed | {e.info["msg"].lower()} | retcode = {e.info["retcode"]} | {e.info["wording"]}'
                )
                return
