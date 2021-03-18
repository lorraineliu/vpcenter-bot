# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List
from botbuilder.core import (
    ConversationState,
    MessageFactory,
    UserState,
    TurnContext,
)
from botbuilder.dialogs import Dialog
from botbuilder.schema import ChannelAccount

from .dialog_bot import DialogBot


class DialogAndWelcomeBot(DialogBot):
    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog,
    ):
        super(DialogAndWelcomeBot, self).__init__(
            conversation_state, user_state, dialog
        )

    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            # Greet anyone that was not the target (recipient) of this message.
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"""欢迎使用 Vpcenter Bot Service
                        \n[1]套餐介绍
                        \n[2]使用教程
                        \n[3]软件下载
                        \n[4]账号到期时间查询
                        \n[5]在线充值（续费）
                        \n[6]常见问题
                        \n[7]用户协议
                        \n[8]关于我们
                        \n[9]人工服务
                        """
                    )
                )
