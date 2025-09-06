import logging
import random
import os
from datetime import datetime
import json

from pyftg import (AIInterface, AudioData, CommandCenter, FrameData, GameData,
                   Key, RoundResult, ScreenData)

logger = logging.getLogger(__name__)

POSSIBLE_ACTIONS = [
    "FORWARD_WALK",
    "DASH",
    "BACK_STEP",
    "CROUCH",
    "JUMP",
    "FOR_JUMP",
    "BACK_JUMP",
    "STAND_GUARD",
    "CROUCH_GUARD",
    "AIR_GUARD",
    "THROW_A",
    "THROW_B",
    "STAND_A",
    "STAND_B",
    "CROUCH_A",
    "CROUCH_B",
    "AIR_A",
    "AIR_B",
    "AIR_DA",
    "AIR_DB",
    "STAND_FA",
    "STAND_FB",
    "CROUCH_FA",
    "CROUCH_FB",
    "AIR_FA",
    "AIR_FB",
    "AIR_UA",
    "AIR_UB",
    "STAND_D_DF_FA",
    "STAND_D_DF_FB",
    "STAND_F_D_DFA",
    "STAND_F_D_DFB",
    "STAND_D_DB_BA",
    "STAND_D_DB_BB",
    "AIR_D_DF_FA",
    "AIR_D_DF_FB",
    "AIR_F_D_DFA",
    "AIR_F_D_DFB",
    "AIR_D_DB_BA",
    "AIR_D_DB_BB",
    "STAND_D_DF_FC",
]

SAVE_DIR = "../state_action_records"
os.makedirs(SAVE_DIR, exist_ok=True)

class CustomAI(AIInterface):
    def __init__(self):
        self.blind_flag = False
        self.width = 96
        self.height = 64
        now = datetime.now()
        self.session_id = now.strftime("%m%d_%H%M%S")
        self.file_path_template = os.path.join(
            SAVE_DIR, f"{self.session_id}_r{{round:02d}}.jsonl"
        )

    def name(self) -> str:
        return self.__class__.__name__

    def is_blind(self) -> bool:
        return self.blind_flag

    def initialize(self, game_data: GameData, player: bool):
        logger.info("initialize")
        self.input_key = Key()
        self.cc = CommandCenter()
        self.player = player

    def get_non_delay_frame_data(self, frame_data: FrameData):
        pass
        
    def input(self):
        return self.input_key
        
    def get_information(self, frame_data: FrameData, is_control: bool):
        self.frame_data = frame_data
        self.cc.set_frame_data(frame_data, self.player)
    
    def get_screen_data(self, screen_data: ScreenData):
        self.screen_data = screen_data
    
    def get_audio_data(self, audio_data: AudioData):
        pass
        
    def processing(self):

        if self.frame_data.empty_flag or self.frame_data.current_frame_number <= 0:
            return
  
        if self.cc.get_skill_flag():
            self.input_key = self.cc.get_skill_key()
            return

        self.input_key.empty()
        self.cc.skill_cancel()

        action = random.choice(POSSIBLE_ACTIONS)
        self.cc.command_call(action)

        self.save_frame_data(self.frame_data.to_dict(), action)

    def save_frame_data(self, frame_data_dict, action):
        """
        현재 프레임 데이터를 JSONL로 저장

        Args:
            frame_data_dict (dict): FrameData를 to_dict()로 변환한 dict
            action (str): AI가 선택한 action
        """
        frame_data_dict['action'] = action

        round_num = frame_data_dict['current_round']
        file_path = self.file_path_template.format(round=round_num)

        with open(file_path, "a") as f:
            f.write(json.dumps(frame_data_dict) + "\n")

                        
    def calculate_distance(self, display_buffer: bytes):
        for y in reversed(range(self.height)):
            # when searching for the same row is over, reset each data
            previousPixel = 0
            leftCharacterX = -1
            rightCharacterX = -1
            for x in range(self.width):
                currentPixel = display_buffer[y * self.width + x]
                # record x coordinate of the character on right side
                if currentPixel and previousPixel == 0 and leftCharacterX != -1:
                    rightCharacterX = x - 1
                    return abs(leftCharacterX - rightCharacterX)
                # record x coordinate of the character on left side
                if previousPixel and currentPixel == 0:
                    leftCharacterX = x - 1
                # update pixel data
                previousPixel = currentPixel
        return -1

    def round_end(self, round_result: RoundResult):
        logger.info(f"round end: {round_result}")
    
    def game_end(self):
        logger.info("game end")
        
    def close(self):
        pass