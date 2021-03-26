from typing import List

from botbuilder.dialogs import (
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    ComponentDialog,
)
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions,TextPrompt
from botbuilder.core import MessageFactory

from data_model import Daydayup


class Dialog007(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(Dialog007, self).__init__(dialog_id or Dialog007.__name__)
        self.DONE_OPTION = 0
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.ask_step,
                    self.search_step,
                ]
            )
        )
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.initial_dialog_id = WaterfallDialog.__name__

    async def ask_step(self,step_context: WaterfallStepContext) -> DialogTurnResult:
        prompt_options = PromptOptions(prompt=MessageFactory.text(f"""请输入您的邮箱地址或输入0返回上一级菜单"""))
        return await step_context.prompt(TextPrompt.__name__, prompt_options)

    async def search_step(self,step_context: WaterfallStepContext) -> DialogTurnResult:
        email = step_context.result
        try:
            done = eval(email) == self.DONE_OPTION
            if done:
                return await step_context.end_dialog(self.DONE_OPTION)
        except Exception:
            pass
        # Confirm the user email input
        await step_context.context.send_activity(MessageFactory.text(f"Thanks {email}"))
        try:
            expire_time = self._check_expire_time(email)
            await step_context.context.send_activity(f"{expire_time}")
        except Exception as e:
            if "DoesNotExist" in e.args[0]:
                await step_context.context.send_activity("Email not found.")
        finally:
            return await step_context.replace_dialog(self.__class__.__name__)

    def _check_expire_time(self, email):
        user = Daydayup.get(email=email)
        return user.expire_in
