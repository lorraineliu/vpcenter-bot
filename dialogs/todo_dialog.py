from typing import List

from botbuilder.dialogs import (
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    ComponentDialog,
)
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions, NumberPrompt
from botbuilder.core import MessageFactory


class TodoDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(TodoDialog, self).__init__(dialog_id or TodoDialog.__name__)
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.promp_step,
                    self.loop_step,
                ]
            )
        )
        self.initial_dialog_id = WaterfallDialog.__name__

    async def promp_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        prompt_options = PromptOptions(prompt=MessageFactory.text(f"""开发中，敬请期待！请按0返回上一级菜单 http://www.baidu.com/"""))
        return await step_context.prompt(NumberPrompt.__name__, prompt_options)

    async def loop_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        selected = step_context.result
        done = selected == 0
        if done:
            return await step_context.end_dialog(selected)
        return await step_context.replace_dialog(self.__class__.__name__)
