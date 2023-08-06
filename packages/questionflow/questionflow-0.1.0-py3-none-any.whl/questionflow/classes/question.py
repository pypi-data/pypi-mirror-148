from typing import Union

from questionflow.classes.answer import Answer


class Question:
    def __init__(self, prompt: str):
        self._prompt = prompt
        self._answer = None

    def __str__(self) -> str:
        return self._prompt

    def __repr__(self) -> str:
        return self._prompt

    def __eq__(self, other: 'Question') -> bool:
        return self._prompt == other._prompt and self.answer == other.answer

    def __hash__(self) -> int:
        return hash(self._prompt)

    def add_answer(self, answer: Answer) -> bool:
        """
        Add an answer to the question.
        :return: True
        """
        self._answer = answer
        return True

    def reset_answer(self) -> None:
        self._answer = None

    @property
    def answer(self) -> Union[Answer, None]:
        return self._answer

    @property
    def prompt(self) -> str:
        return self._prompt

    @property
    def confirmation_prompt(self) -> Union[str, None]:
        if not self.answer:
            return None
        return f"Is '{self.answer.value}' correct?"
