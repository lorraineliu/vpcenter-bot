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

from dialogs.instruction_dialog import InstructionDialog
from dialogs.download_dialog import DownloadDialog
from dialogs.account_expiration_dialog import AccountExpirationDialog

class CustomTopLevelDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(CustomTopLevelDialog, self).__init__(dialog_id or CustomTopLevelDialog.__name__)
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(InstructionDialog(InstructionDialog.__name__))
        self.add_dialog(DownloadDialog(DownloadDialog.__name__))
        self.add_dialog(AccountExpirationDialog(AccountExpirationDialog.__name__))

        self.add_dialog(
            WaterfallDialog(
                "VPCenterDialog",
                [
                    self.action_step,
                    self.start_sub_step,
                    self.end_step,
                ]
            )
        )

        self.initial_dialog_id = "VPCenterDialog"

    async def action_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        prompt_options = PromptOptions(
            prompt=MessageFactory.text("请输入您的执行编号，可选1或2或3")
        )
        return await step_context.prompt(NumberPrompt.__name__, prompt_options)

    async def start_sub_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        user_action = step_context.result

        if user_action == 1:
            return await step_context.begin_dialog(InstructionDialog.__name__)
        elif user_action ==2:
            return await step_context.begin_dialog(DownloadDialog.__name__)
        elif user_action == 3:
            return await step_context.begin_dialog(AccountExpirationDialog.__name__)
        return await step_context.next([])

    async def end_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        selected = step_context.result
        if selected in ['[000]返回']:
            return await step_context.replace_dialog(CustomTopLevelDialog.__name__)
        # Exit the dialog.
        return await step_context.end_dialog()
