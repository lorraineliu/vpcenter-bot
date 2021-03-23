import json
import os.path

from typing import List

from botbuilder.dialogs import (
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    ComponentDialog,
)
from botbuilder.dialogs.prompts import ChoicePrompt, PromptOptions
from botbuilder.dialogs.choices import Choice, FoundChoice
from botbuilder.core import MessageFactory, CardFactory
from botbuilder.schema import Attachment, ChannelAccount



class InstructionDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(InstructionDialog, self).__init__(
            dialog_id or InstructionDialog.__name__
        )

        self.DONE_OPTION = '[000]返回'
        self.sub_action_options = [
            '[101]套餐1',
            '[102]套餐2',
            '[103]套餐3',
        ]

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
        selected: [str] = step_context.options if step_context.options is not None else []
        msg = (f"请选择套餐编号,或者`{self.DONE_OPTION}`返回上一级菜单")

        # create a list of options to choose, with already selected items removed.
        options = self.sub_action_options.copy()
        options.append(self.DONE_OPTION)

        # prompt with the list of choices
        prompt_options = PromptOptions(
            prompt=MessageFactory.text(msg),
            retry_prompt=MessageFactory.text(msg),
            choices=self._to_choices(options),
        )
        return await step_context.prompt(ChoicePrompt.__name__, prompt_options)

    def _to_choices(self, choices: [str]) -> List[Choice]:
        choice_list: List[Choice] = []
        for choice in choices:
            choice_list.append(Choice(value=choice))
        return choice_list

    async def loop_step(self, step_context:WaterfallStepContext) -> DialogTurnResult:
        choice: FoundChoice = step_context.result
        selected = choice.value
        done = selected == self.DONE_OPTION
        if done:
            return await step_context.end_dialog(selected)
        if selected in self.sub_action_options:
            card = self.create_adaptive_card_attachment(selected)
            response = MessageFactory.attachment(card)
            await step_context.context.send_activity(response)
        return await step_context.replace_dialog(InstructionDialog.__name__)

    # Load attachment from file.
    def create_adaptive_card_attachment(self, card_name):
        relative_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(relative_path, f"""../cards/1/{card_name}.json""")
        with open(path) as in_file:
            card = json.load(in_file)
        return CardFactory.adaptive_card(card)
