import pytest

from src.domain.game import Game, GameColor, MaxTriesReachedException


class TestGame:

    @pytest.fixture
    def instance(self) -> Game:
        instance = Game(
            1,
            GameColor.RED.value + GameColor.GREEN.value
            + GameColor.GREEN.value + GameColor.BLUE.value
        )

        return instance

    def test_should_create(self, instance: Game):
        assert bool(instance) is True

    def test_rggb_rggb_should_return_4_0(self, instance: Game):
        expected_result = 4, 0

        result = instance.check_guess(instance.code)

        assert result == expected_result

    def test_rrrr_byob_should_return_0_0(self, instance: Game):
        expected_result = 0, 0
        instance.code = GameColor.RED.value * 4

        result = instance.check_guess(
            GameColor.BLUE.value + GameColor.YELLOW.value
            + GameColor.ORANGE.value + GameColor.BLUE.value
        )

        assert result == expected_result

    def test_gbbr_gbrb_should_return_2_2(self, instance: Game):
        expected_result = 2, 2
        instance.code = GameColor.GREEN.value + GameColor.BLUE.value\
            + GameColor.BLUE.value + GameColor.RED.value

        result = instance.check_guess(
            GameColor.GREEN.value + GameColor.BLUE.value
            + GameColor.RED.value + GameColor.BLUE.value
        )

        assert result == expected_result

    def test_bbbr_rbgg_should_return_1_1(self, instance: Game):
        expected_result = 1, 1
        instance.code = GameColor.BLUE.value + GameColor.BLUE.value \
            + GameColor.BLUE.value + GameColor.RED.value

        result = instance.check_guess(
            GameColor.RED.value + GameColor.BLUE.value
            + GameColor.GREEN.value + GameColor.GREEN.value
        )

        assert result == expected_result

    def test_rbgg_bbbr_should_return_1_1(self, instance: Game):
        expected_result = 1, 1
        instance.code = GameColor.RED.value + GameColor.BLUE.value \
            + GameColor.GREEN.value + GameColor.GREEN.value

        result = instance.check_guess(
            GameColor.BLUE.value + GameColor.BLUE.value
            + GameColor.BLUE.value + GameColor.RED.value
        )

        assert result == expected_result

    def test_wbwb_bwbw_should_return_0_4(self, instance: Game):
        expected_result = 0, 4
        instance.code = GameColor.WHITE.value + GameColor.BLUE.value \
            + GameColor.WHITE.value + GameColor.BLUE.value

        result = instance.check_guess(
            GameColor.BLUE.value + GameColor.WHITE.value
            + GameColor.BLUE.value + GameColor.WHITE.value
        )

        assert result == expected_result

    def test_ooow_owww_should_return_2_0(self, instance: Game):
        expected_result = 2, 0
        instance.code = GameColor.ORANGE.value + GameColor.ORANGE.value \
            + GameColor.ORANGE.value + GameColor.WHITE.value

        result = instance.check_guess(
            GameColor.ORANGE.value + GameColor.WHITE.value
            + GameColor.WHITE.value + GameColor.WHITE.value
        )

        assert result == expected_result

    def test_should_raise_max_tries_reached(self, instance: Game):
        instance.tries = instance.max_tries

        with pytest.raises(MaxTriesReachedException):
            instance.check_guess('')

    def test_should_mark_guessed_to_true(self, instance: Game):
        instance.check_guess(instance.code)

        assert instance.guessed is True

    def test_should_generate_code(self):
        instance = Game()

        assert len(instance.code) == instance.code_length
