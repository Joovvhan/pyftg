import logging
import random

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

class CustomAI(AIInterface):
    def __init__(self):
        self.blind_flag = False
        self.width = 96
        self.height = 64

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

        print("This function is called every frame")

        if self.frame_data.empty_flag or self.frame_data.current_frame_number <= 0:
            return
  
        if self.cc.get_skill_flag():
            self.input_key = self.cc.get_skill_key()
            return

        self.input_key.empty()
        self.cc.skill_cancel()

        # calculate the distance
        # try:
        #     distance = self.calculate_distance(self.screen_data.display_bytes)
        # except:
        #     distance = 0
        # if distance == -1:
        #     self.cc.command_call("STAND_A") # default action
        # else:
        #     close = 80 * self.width / 960
        #     far = 200 * self.width / 960
        #     # conduct action according to the distance based on pixel data
        #     if distance < close:
        #         self.cc.command_call("CROUCH_B")
        #     elif distance >= close and distance < far:
        #         self.cc.command_call("STAND_FB")
        #     else:
        #         self.cc.command_call("STAND_D_DF_FA")
        
        print(f"{self.frame_data.character_data=}")
        print(f"{self.frame_data.projectile_data=}")

        # self.frame_data.character_data = [
        #     CharacterData(
        #         player_number=True, hp=340, energy=38, x=474, y=537,
        #         left=454, right=494, top=435, bottom=640, speed_x=0, speed_y=0,
        #         state=<State.STAND: 'stand'>, action=<Action.STAND_D_DF_FA: 'stand_d_df_fa'>,
        #         front=True, control=False,
        #         attack_data=AttackData(
        #             setting_hit_area=HitArea(left=0, right=0, top=0, bottom=0),
        #             setting_speed_x=0, setting_speed_y=0,
        #             current_hit_area=HitArea(left=0, right=0, top=0, bottom=0),
        #             current_frame=-1, player_number=True, speed_x=0, speed_y=0,
        #             start_up=0, active=0, hit_damage=0, guard_damage=0,
        #             start_add_energy=0, hit_add_energy=0, guard_add_energy=0,
        #             give_energy=0, impact_x=0, impact_y=0, give_guard_recov=0,
        #             attack_type=0, down_prop=False, is_projectile=False,
        #             is_live=False, empty_flag=True, identifier=''
        #         ),
        #         remaining_frame=9, hit_confirm=False,
        #         graphic_size_x=400, graphic_size_y=320, graphic_adjust_x=140,
        #         hit_count=0, last_hit_frame=623,
        #         projectile_attack=[
        #             AttackData(setting_hit_area=HitArea(left=205, right=250, top=175, bottom=195),
        #                     setting_speed_x=3, setting_speed_y=0,
        #                     current_hit_area=HitArea(left=635, right=680, top=510, bottom=530),
        #                     current_frame=32, player_number=True, speed_x=3, speed_y=0,
        #                     start_up=20, active=150, hit_damage=5, guard_damage=2,
        #                     start_add_energy=-5, hit_add_energy=3, guard_add_energy=5,
        #                     give_energy=5, impact_x=10, impact_y=0, give_guard_recov=5,
        #                     attack_type=1, down_prop=False, is_projectile=True, is_live=True,
        #                     empty_flag=False, identifier='ff6438e3-ff1a-4239-909b-beb2f467dc64'
        #             ),
        #             AttackData(setting_hit_area=HitArea(left=0, right=0, top=0, bottom=0),
        #                     setting_speed_x=0, setting_speed_y=0,
        #                     current_hit_area=HitArea(left=0, right=0, top=0, bottom=0),
        #                     current_frame=-1, player_number=True, speed_x=0, speed_y=0,
        #                     start_up=0, active=0, hit_damage=0, guard_damage=0,
        #                     start_add_energy=0, hit_add_energy=0, guard_add_energy=0,
        #                     give_energy=0, impact_x=0, impact_y=0, give_guard_recov=0,
        #                     attack_type=0, down_prop=False, is_projectile=False, is_live=False,
        #                     empty_flag=True, identifier=''),
        #             AttackData(setting_hit_area=HitArea(left=0, right=0, top=0, bottom=0),
        #                     setting_speed_x=0, setting_speed_y=0,
        #                     current_hit_area=HitArea(left=0, right=0, top=0, bottom=0),
        #                     current_frame=-1, player_number=True, speed_x=0, speed_y=0,
        #                     start_up=0, active=0, hit_damage=0, guard_damage=0,
        #                     start_add_energy=0, hit_add_energy=0, guard_add_energy=0,
        #                     give_energy=0, impact_x=0, impact_y=0, give_guard_recov=0,
        #                     attack_type=0, down_prop=False, is_projectile=False, is_live=False,
        #                     empty_flag=True, identifier='')
        #         ]
        #     ),
        #     CharacterData(
        #         player_number=False, hp=345, energy=85, x=778, y=557,
        #         left=758, right=798, top=475, bottom=640, speed_x=0, speed_y=0,
        #         state=<State.CROUCH: 'crouch'>, action=<Action.CROUCH_B: 'crouch_b'>,
        #         front=False, control=False,
        #         attack_data=AttackData(setting_hit_area=HitArea(left=0, right=0, top=0, bottom=0),
        #                             setting_speed_x=0, setting_speed_y=0,
        #                             current_hit_area=HitArea(left=0, right=0, top=0, bottom=0),
        #                             current_frame=-1, player_number=True, speed_x=0, speed_y=0,
        #                             start_up=0, active=0, hit_damage=0, guard_damage=0,
        #                             start_add_energy=0, hit_add_energy=0, guard_add_energy=0,
        #                             give_energy=0, impact_x=0, impact_y=0, give_guard_recov=0,
        #                             attack_type=0, down_prop=False, is_projectile=False,
        #                             is_live=False, empty_flag=True, identifier=''),
        #         remaining_frame=15, hit_confirm=False,
        #         graphic_size_x=400, graphic_size_y=320, graphic_adjust_x=140,
        #         hit_count=0, last_hit_frame=487,
        #         projectile_attack=[
        #             AttackData(setting_hit_area=HitArea(left=0, right=0, top=0, bottom=0),
        #                     setting_speed_x=0, setting_speed_y=0,
        #                     current_hit_area=HitArea(left=0, right=0, top=0, bottom=0),
        #                     current_frame=-1, player_number=True, speed_x=0, speed_y=0,
        #                     start_up=0, active=0, hit_damage=0, guard_damage=0,
        #                     start_add_energy=0, hit_add_energy=0, guard_add_energy=0,
        #                     give_energy=0, impact_x=0, impact_y=0, give_guard_recov=0,
        #                     attack_type=0, down_prop=False, is_projectile=False, is_live=False,
        #                     empty_flag=True, identifier=''),
        #             AttackData(setting_hit_area=HitArea(left=0, right=0, top=0, bottom=0),
        #                     setting_speed_x=0, setting_speed_y=0,
        #                     current_hit_area=HitArea(left=0, right=0, top=0, bottom=0),
        #                     current_frame=-1, player_number=True, speed_x=0, speed_y=0,
        #                     start_up=0, active=0, hit_damage=0, guard_damage=0,
        #                     start_add_energy=0, hit_add_energy=0, guard_add_energy=0,
        #                     give_energy=0, impact_x=0, impact_y=0, give_guard_recov=0,
        #                     attack_type=0, down_prop=False, is_projectile=False, is_live=False,
        #                     empty_flag=True, identifier=''),
        #             AttackData(setting_hit_area=HitArea(left=0, right=0, top=0, bottom=0),
        #                     setting_speed_x=0, setting_speed_y=0,
        #                     current_hit_area=HitArea(left=0, right=0, top=0, bottom=0),
        #                     current_frame=-1, player_number=True, speed_x=0, speed_y=0,
        #                     start_up=0, active=0, hit_damage=0, guard_damage=0,
        #                     start_add_energy=0, hit_add_energy=0, guard_add_energy=0,
        #                     give_energy=0, impact_x=0, impact_y=0, give_guard_recov=0,
        #                     attack_type=0, down_prop=False, is_projectile=False, is_live=False,
        #                     empty_flag=True, identifier='')
        #         ]
        #     )
        # ]

        # self.frame_data.projectile_data = [
        #     AttackData(
        #         setting_hit_area=HitArea(left=205, right=250, top=175, bottom=195),
        #         setting_speed_x=3, setting_speed_y=0,
        #         current_hit_area=HitArea(left=632, right=677, top=510, bottom=530),
        #         current_frame=31, player_number=True, speed_x=3, speed_y=0,
        #         start_up=20, active=150, hit_damage=5, guard_damage=2,
        #         start_add_energy=-5, hit_add_energy=3, guard_add_energy=5,
        #         give_energy=5, impact_x=10, impact_y=0, give_guard_recov=5,
        #         attack_type=1, down_prop=False, is_projectile=True, is_live=True,
        #         empty_flag=False, identifier='ff6438e3-ff1a-4239-909b-beb2f467dc64'
        #     )
        # ]

        action = random.choice(POSSIBLE_ACTIONS)
        self.cc.command_call(action)
                        
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