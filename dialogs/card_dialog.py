import json
import os.path

from botbuilder.dialogs import (
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    ComponentDialog,
)
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions, NumberPrompt
from botbuilder.core import MessageFactory, CardFactory
from .menu import *

class CardDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None, menu_str: str = None):
        super(CardDialog, self).__init__(dialog_id or CardDialog.__name__)
        self.prompt = menu_str
        self.options = menu_str.split()
        self.DONE_OPTION = 0
        self.sub_action_options = [int(i[1:4]) for i in self.options[:-1]]

        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.selection_step,
                    self.loop_step
                ]
            )
        )
        self.initial_dialog_id = WaterfallDialog.__name__

    async def selection_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        prompt_options = PromptOptions(prompt=MessageFactory.text(self.prompt))
        return await step_context.prompt(NumberPrompt.__name__, prompt_options)

    async def loop_step(self, step_context:WaterfallStepContext) -> DialogTurnResult:
        selected = step_context.result
        done = selected == self.DONE_OPTION
        if done:
            return await step_context.end_dialog(selected)
        if selected in self.sub_action_options:
            card = self._create_adaptive_card_attachment(selected)
            response = MessageFactory.attachment(card)
            await step_context.context.send_activity(response)
        return await step_context.replace_dialog(self.__class__.__name__)

    # Load attachment from file.
    def _create_adaptive_card_attachment(self, card_name):
        relative_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(relative_path, f"""../cards/{str(card_name)[0]}/{str(card_name)}.json""")
        with open(path) as in_file:
            card = json.load(in_file)
        return CardFactory.adaptive_card(card)


class Dialog001(CardDialog):
    def __init__(self, dialog_id: str = None):
        super(Dialog001, self).__init__(dialog_id or Dialog001.__name__, MENU_001)

class Dialog002(CardDialog):
    def __init__(self, dialog_id: str = None):
        super(Dialog002, self).__init__(dialog_id or Dialog002.__name__, MENU_002)

class Dialog003(CardDialog):
    def __init__(self, dialog_id: str = None):
        super(Dialog003, self).__init__(dialog_id or Dialog003.__name__, MENU_003)

class Dialog004(CardDialog):
    def __init__(self, dialog_id: str = None):
        super(Dialog004, self).__init__(dialog_id or Dialog004.__name__, MENU_004)

class Dialog005(CardDialog):
    def __init__(self, dialog_id: str = None):
        super(Dialog005, self).__init__(dialog_id or Dialog005.__name__, MENU_005)

class Dialog006(CardDialog):
    def __init__(self, dialog_id: str = None):
        super(Dialog006, self).__init__(dialog_id or Dialog006.__name__, MENU_006)

class Dialog007(CardDialog):
    def __init__(self, dialog_id: str = None):
        super(Dialog007, self).__init__(dialog_id or Dialog007.__name__, MENU_007)

class Dialog008(CardDialog):
    def __init__(self, dialog_id: str = None):
        super(Dialog008, self).__init__(dialog_id or Dialog008.__name__, MENU_008)

class Dialog009(CardDialog):
    def __init__(self, dialog_id: str = None):
        super(Dialog009, self).__init__(dialog_id or Dialog009.__name__, MENU_009)
