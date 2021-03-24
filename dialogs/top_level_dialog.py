# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import MessageFactory
from botbuilder.dialogs import (
    WaterfallDialog,
    DialogTurnResult,
    WaterfallStepContext,
    ComponentDialog,
)
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt

from .card_dialog import *


class CustomTopLevelDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(CustomTopLevelDialog, self).__init__(dialog_id or CustomTopLevelDialog.__name__)
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(Dialog001(Dialog001.__name__))
        self.add_dialog(Dialog002(Dialog002.__name__))
        self.add_dialog(Dialog003(Dialog003.__name__))
        self.add_dialog(Dialog004(Dialog004.__name__))
        self.add_dialog(Dialog005(Dialog005.__name__))
        self.add_dialog(Dialog006(Dialog006.__name__))
        self.add_dialog(Dialog007(Dialog007.__name__))
        self.add_dialog(Dialog008(Dialog008.__name__))
        self.add_dialog(Dialog009(Dialog009.__name__))


        self.add_dialog(
            WaterfallDialog(
                "VPCenterDialog",
                [
                    self.action_step,
                    self.start_sub_step,
                    self.loop_step,
                ]
            )
        )

        self.initial_dialog_id = "VPCenterDialog"

    async def action_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        prompt_options = PromptOptions(prompt=MessageFactory.text(MAIN_MENU))
        return await step_context.prompt(NumberPrompt.__name__, prompt_options)

    async def start_sub_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_action = step_context.result

        if user_action == 1:
            return await step_context.begin_dialog(Dialog001.__name__)
        elif user_action == 2:
            return await step_context.begin_dialog(Dialog002.__name__)
        elif user_action == 3:
            return await step_context.begin_dialog(Dialog003.__name__)
        elif user_action == 4:
            return await step_context.begin_dialog(Dialog004.__name__)
        elif user_action == 5:
            return await step_context.begin_dialog(Dialog005.__name__)
        elif user_action == 6:
            return await step_context.begin_dialog(Dialog006.__name__)
        elif user_action == 8:
            return await step_context.begin_dialog(Dialog008.__name__)
        elif user_action == 9:
            return await step_context.begin_dialog(Dialog009.__name__)
        #  待开发二级菜单
        elif user_action in [7]:
            return await step_context.begin_dialog(Dialog007.__name__)
        return await step_context.next(user_action)

    async def loop_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        selected = step_context.result
        if selected == 0:
            return await step_context.end_dialog()
        return await step_context.replace_dialog(CustomTopLevelDialog.__name__)
