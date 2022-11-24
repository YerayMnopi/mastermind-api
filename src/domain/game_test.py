from unittest.mock import MagicMock

import pytest
import requests

from src.domain.game import Game, MaxTriesReachedException, GameColor
from src.settings import get_settings


class TestGame:

    @pytest.fixture
    def instance(self) -> Game:
        instance = Game(
            1,
            f'{GameColor.RED.value}{GameColor.GREEN.value}{GameColor.GREEN.value}{GameColor.BLUE.value}',
            3,
            0
        )

        return instance

    def test_should_create(self, instance: Game):
        assert bool(instance) is True

    def test_RGGB_RGGB_should_return_4_0(self, instance: Game):
        expected_result = 4, 0

        result = instance.check_guess(instance.code)

        assert result.values() == expected_result

    def test_RRRR_BYOB_should_return_0_0(self, instance: Game):
        expected_result = 0, 0
        instance.code = f'{GameColor.RED.value}{GameColor.RED.value}{GameColor.RED.value}{GameColor.RED.value}'

        result = instance.check_guess(
            f'{GameColor.BLUE.value}{GameColor.YELLOW.value}{GameColor.ORANGE.value}{GameColor.BLUE.value}'
        )

        assert result.values() == expected_result

    def test_GBBR_GBRB_should_return_2_2(self, instance: Game):
        expected_result = 2, 2
        instance.code = f'{GameColor.GREEN.value}{GameColor.BLUE.value}{GameColor.BLUE.value}{GameColor.RED.value}'

        result = instance.check_guess(
            f'{GameColor.GREEN.value}{GameColor.BLUE.value}{GameColor.RED.value}{GameColor.BLUE.value}'
        )

        assert result.values() == expected_result

    def test_BBBR_RBGG_should_return_1_1(self, instance: Game):
        expected_result = 1, 1
        instance.code = f'{GameColor.BLUE.value}{GameColor.BLUE.value}{GameColor.BLUE.value}{GameColor.RED.value}'

        result = instance.check_guess(
            f'{GameColor.RED.value}{GameColor.BLUE.value}{GameColor.GREEN.value}{GameColor.GREEN.value}'
        )

        assert result.values() == expected_result

    def test_RBGG_BBBR_should_return_1_1(self, instance: Game):
        expected_result = 1, 1
        instance.code = f'{GameColor.RED.value}{GameColor.BLUE.value}{GameColor.GREEN.value}{GameColor.GREEN.value}'

        result = instance.check_guess(
            f'{GameColor.BLUE.value}{GameColor.BLUE.value}{GameColor.BLUE.value}{GameColor.RED.value}'
        )

        assert result.values() == expected_result
        
    def test_WBWB_BWBW_should_return_0_4(self, instance: Game):
        expected_result = 0, 4
        instance.code = f'{GameColor.WHITE.value}{GameColor.BLUE.value}{GameColor.WHITE.value}{GameColor.BLUE.value}'

        result = instance.check_guess(
            f'{GameColor.BLUE.value}{GameColor.WHITE.value}{GameColor.BLUE.value}{GameColor.WHITE.value}'
        )

        assert result.values() == expected_result
    
    def test_OOOW_OWWW_should_return_2_0(self, instance: Game):
        expected_result = 2, 0
        instance.code = f'{GameColor.ORANGE.value}{GameColor.ORANGE.value}{GameColor.ORANGE.value}{GameColor.WHITE.value}'

        result = instance.check_guess(
            f'{GameColor.ORANGE.value}{GameColor.WHITE.value}{GameColor.WHITE.value}{GameColor.WHITE.value}'
        )

        assert result.values() == expected_result
        
    
    def test_should_raise_max_tries_reached(self, instance: Game):
        instance.tries = instance.max_tries
        
        with pytest.raises(MaxTriesReachedException):
            instance.check_guess('')