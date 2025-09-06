from glob import glob
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def visualize_frame(frame_data, ax):
    """
    한 프레임 데이터를 시각화합니다.
    캐릭터, HP/EN/Action, 공격 히트박스, 투사체를 표시합니다.
    공격 히트박스는 캐릭터 중심 좌표 기준으로 변환됩니다.

    Args:
        frame_data (dict): 한 프레임의 상태 액션 데이터
        ax (matplotlib.axes.Axes): 시각화를 위한 Axes 객체
    """
    characters = frame_data['character_data']
    projectiles = frame_data.get('projectile_data', [])

    # 좌표/제목/축
    ax.set_xlim(0, 960)
    ax.set_ylim(0, 720)
    ax.set_title(f"Frame {frame_data.get('current_frame_number', '?')} - Round {frame_data.get('current_round', '?')}")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    # 캐릭터 표시
    for char in characters:
        x, y = char['x'], char['y']  # 캐릭터 중심 좌표
        left, right, top, bottom = char['left'], char['right'], char['top'], char['bottom']
        front = char['front']

        # 캐릭터 사각형
        rect = patches.Rectangle(
            (left, top), right-left, bottom-top, linewidth=2,
            edgecolor='blue' if char['player_number'] else 'red', facecolor='none'
        )
        ax.add_patch(rect)

        # 시선 방향 화살표
        dx = 20 if front else -20
        ax.arrow(x, y, dx, 0, head_width=10, head_length=10, fc='green', ec='green')

        # HP / Energy / Action 텍스트
        ax.text(x, top-15, f"HP:{char['hp']}", color='red', fontsize=10, ha='center')
        ax.text(x, top-30, f"EN:{char['energy']}", color='blue', fontsize=10, ha='center')
        ax.text(x, bottom+15, f"Action:{char.get('action', '?')}", color='black', fontsize=10, ha='center')

        # 캐릭터 공격 & 투사체 공격 히트박스 표시
        attack_list = [char.get('attack_data')] + char.get('projectile_attack', [])
        for atk in attack_list:
            if atk is None:
                continue

            hit_area = atk.get('current_hit_area')  # ✅ current_hit_area 사용

            abs_left   = hit_area['left']
            abs_right  = hit_area['right']
            abs_top    = hit_area['top']
            abs_bottom = hit_area['bottom']

            # ✅ player_number에 따라 색상 변경
            color = 'orange' if atk.get('player_number') else 'magenta'

            atk_rect = patches.Rectangle(
                (abs_left, abs_top),
                abs_right - abs_left,
                abs_bottom - abs_top,
                linewidth=1, edgecolor=color, facecolor='none', linestyle='--'
            )
            ax.add_patch(atk_rect)

            # 공격 속성 텍스트
            rem_frame = atk.get('remaining_frame', atk.get('current_frame', '?'))

            if rem_frame < 0:
                continue

            hit_confirm = atk.get('hit_confirm', False)
            active = atk.get('active', 0)
            hit_damage = atk.get('hit_damage', 0)
            guard_damage = atk.get('guard_damage', 0)
            start_up = atk.get('start_up', 0)

            ax.text(
                abs_left, abs_top - 5,
                f"RF:{rem_frame} Hit:{hit_confirm} Act:{active}\n"
                f"HD:{hit_damage} GD:{guard_damage} SU:{start_up}",
                color=color, fontsize=8  # ✅ 텍스트도 같은 색상으로
            )

        # 독립 투사체 표시
        # for proj in projectiles:
        #     hit_area = proj.get('current_hit_area')  # ✅ 여기도 current_hit_area로 변경
        #     proj_rect = patches.Rectangle(
        #         (hit_area['left'], hit_area['top']),
        #         hit_area['right'] - hit_area['left'],
        #         hit_area['bottom'] - hit_area['top'],
        #         linewidth=1, edgecolor='purple', facecolor='none', linestyle=':'
        #     )
        #     ax.add_patch(proj_rect)

        #     rem_frame = proj.get('remaining_frame', proj.get('current_frame', '?'))
        #     hit_confirm = proj.get('hit_confirm', False)
        #     active = proj.get('active', 0)
        #     hit_damage = proj.get('hit_damage', 0)
        #     guard_damage = proj.get('guard_damage', 0)
        #     start_up = proj.get('start_up', 0)

        #     ax.text(
        #         hit_area['left'], hit_area['top'] - 5,
        #         f"RF:{rem_frame} Hit:{hit_confirm} Act:{active}\n"
        #         f"HD:{hit_damage} GD:{guard_damage} SU:{start_up}",
        #         color='purple', fontsize=8
        #     )


    ax.invert_yaxis()
    ax.grid(True)



if __name__ == "__main__":

    state_action_records_path = "../state_action_records/*.jsonl"
    state_action_records = glob(state_action_records_path)
    if not state_action_records:
        raise FileNotFoundError("No state-action records found.")

    # 첫 번째 파일 선택
    file_path = state_action_records[2]

    # JSONL 한 줄씩 읽기
    with open(file_path, "r") as f:

        fig, ax = plt.subplots(figsize=(12, 8))

        for line in f:
            frame_data = json.loads(line)
            
            ax.cla()
            visualize_frame(frame_data, ax)
            # plt.pause(0.1)
            plt.pause(1.0)