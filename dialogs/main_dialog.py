# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.core import MessageFactory, UserState

from dialogs.top_level_dialog import CustomTopLevelDialog


class CustomMainDialog(ComponentDialog):
    def __init__(self, user_status: UserState):
        super(CustomMainDialog, self).__init__(CustomMainDialog.__name__)
        self.user_state = user_status
        self.add_dialog(CustomTopLevelDialog(CustomTopLevelDialog.__name__))
        self.add_dialog(
            WaterfallDialog("VPCenterDialog", [self.initial_step, self.final_step])
        )
        self.initial_dialog_id = "VPCenterDialog"

    async def initial_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.begin_dialog(CustomTopLevelDialog.__name__)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        status = f"""感谢使用!"""

        await step_context.context.send_activity(MessageFactory.text(status))

        return await step_context.end_dialog()
