from glob import glob
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

def is_valid_attack(atk: dict, check_bbox: bool = True) -> bool:
    """
    공격/투사체 데이터가 유효한지 판별합니다.

    기준:
    - empty_flag가 False
    - current_frame >= 0
    - (투사체의 경우 is_live도 확인 가능)
    - check_bbox=True이면 current_hit_area의 폭과 높이가 0인지 확인

    Args:
        atk (dict): AttackData 또는 dict 형식의 공격 데이터
        check_bbox (bool): True면 폭/높이 0인 BBOX를 무효 처리

    Returns:
        bool: 유효하면 True, 아니면 False
    """
    if atk is None:
        return False
    
    # dict로 들어오는 경우와 객체로 들어오는 경우 처리
    empty_flag = atk.get("empty_flag", True) if isinstance(atk, dict) else getattr(atk, "empty_flag", True)
    current_frame = atk.get("current_frame", -1) if isinstance(atk, dict) else getattr(atk, "current_frame", -1)
    is_projectile = atk.get("is_projectile", False) if isinstance(atk, dict) else getattr(atk, "is_projectile", False)
    is_live = atk.get("is_live", False) if isinstance(atk, dict) else getattr(atk, "is_live", False)

    if empty_flag:
        return False
    
    if current_frame < 0:
        return False

    if is_projectile and not is_live:
        return False
    
    # required_keys = ['remaining_frame', 'hit_confirm']
    # if not all(k in atk for k in required_keys):
    #     return False

    # 옵션: BBOX 유효성 체크
    if check_bbox:
        hit_area = atk.get("current_hit_area", {})
        width = hit_area.get("right", 0) - hit_area.get("left", 0)
        height = hit_area.get("bottom", 0) - hit_area.get("top", 0)
        if width <= 0 or height <= 0:
            return False

    return True


def debug_attack_projectile_lengths(file_path: str):
    """
    JSONL 파일 전체를 읽어서 각 프레임의 attack_data, projectile_attack 길이를
    Player 0 / Player 1 정보를 같은 줄에 고정 폭으로 출력.
    Valid Attack과 Valid Projectile 개수도 함께 표시합니다.

    출력 예시:
    Frame 9    (Round 1) || P0 | Atk: Present (1/1) | Proj: 3 (1/3) || P1 | Atk: Present (1/1) | Proj: 3 (3/3)
    """
    with open(file_path, "r") as f:
        for line in f:
            frame_data = json.loads(line)
            frame_num = frame_data.get("current_frame_number", "?")
            round_num = frame_data.get("current_round", "?")

            characters = sorted(
                frame_data.get("character_data", []),
                key=lambda c: c.get("player_number", 0)
            )

            row_parts = []
            for char in characters:
                atk = char.get("attack_data")
                proj = char.get("projectile_attack", [])

                # 기존 정보
                atk_info = "None" if atk is None else "Present"
                proj_len = len(proj) if proj is not None else 0

                # Valid 체크
                valid_atk_count = 1 if is_valid_attack(atk) else 0
                valid_proj_count = sum(is_valid_attack(p) for p in proj)

                part = (
                    "P{player:<2} | Atk: {atk:<8} ({v_atk}/1) | "
                    "Proj: {proj:<2} ({v_proj}/{total_proj})"
                ).format(
                    player=char.get("player_number", "?"),
                    atk=atk_info,
                    v_atk=valid_atk_count,
                    proj=proj_len,
                    v_proj=valid_proj_count,
                    total_proj=proj_len
                )

                row_parts.append(part)

            print(f"Frame {frame_num:<4} (Round {round_num}) || " + " || ".join(row_parts))


def debug_attack_bboxes(file_path: str):
    """
    JSONL 파일 전체를 읽어서 각 프레임의 attack_data, projectile_attack BBOX 정보를
    Player 0 / Player 1 기준으로 출력.
    """
    with open(file_path, "r") as f:
        for line in f:
            frame_data = json.loads(line)
            frame_num = frame_data.get("current_frame_number", "?")
            round_num = frame_data.get("current_round", "?")

            characters = sorted(
                frame_data.get("character_data", []),
                key=lambda c: c.get("player_number", 0)
            )

            row_parts = []
            for char in characters:
                atk = char.get("attack_data")
                proj = char.get("projectile_attack", [])

                # 단일 공격 BBOX
                if atk is None:
                    atk_bbox_str = "None"
                elif not is_valid_attack(atk):
                    atk_bbox_str = "Invalid"
                else:
                    hit_area = atk.get('current_hit_area')
                    if hit_area is None:
                        atk_bbox_str = "No BBOX"
                    else:
                        atk_bbox_str = f"L:{hit_area['left']} R:{hit_area['right']} T:{hit_area['top']} B:{hit_area['bottom']}"

                # 투사체 BBOX
                proj_bbox_str_list = []
                for p in proj:
                    if p is None or not is_valid_attack(p):
                        proj_bbox_str_list.append("Invalid")
                        continue
                    hit_area = p.get('current_hit_area')
                    if hit_area is None:
                        proj_bbox_str_list.append("No BBOX")
                    else:
                        proj_bbox_str_list.append(f"L:{hit_area['left']} R:{hit_area['right']} T:{hit_area['top']} B:{hit_area['bottom']}")

                proj_bbox_str = "; ".join(proj_bbox_str_list) if proj_bbox_str_list else "None"

                part = (
                    "P{player:<2} | Atk: {atk:<25} | Proj: {proj}"
                ).format(
                    player=char.get("player_number", "?"),
                    atk=atk_bbox_str,
                    proj=proj_bbox_str
                )
                row_parts.append(part)

            print(f"Frame {frame_num:<4} (Round {round_num}) || " + " || ".join(row_parts))


def filter_frame_data(frame_data):
    """
    시각화용 필수 정보만 추출 및 유효성 검증
    - 원본 frame_data는 변형하지 않음
    - 유효하지 않은 공격/투사체는 제외
    """

    # ---------- 시각화에 필요한 필수 키 ----------
    char_required = [
        'x','y','left','right','top','bottom',
        'player_number','front','hp','energy','action',
        'speed_x','speed_y'
    ]

    attack_required = [
        'current_hit_area', 'player_number', 'current_frame',
        'active','hit_damage','guard_damage','start_up',
        "empty_flag", "is_projectile", "is_live",
        # "right", "left", "top", "bottom",
        # 'remaining_frame', 'hit_confirm',
    ]

    # ---------- 캐릭터 필수 정보만 저장 ----------
    filtered_characters = []

    for char in frame_data.get('character_data', []):
        # 필수 키 존재 여부 확인
        missing = [k for k in char_required if k not in char]
        if missing:
            raise ValueError(f"Character missing required fields {missing}: {char}")

        filtered_char = {k: char[k] for k in char_required}

        # ---------- attack_data 필수 정보 ----------
        atk = char.get('attack_data')
        if atk and is_valid_attack(atk):
            missing_atk = [k for k in attack_required if k not in atk or atk[k] is None]
            if missing_atk:
                raise ValueError(f"Attack missing required fields {missing_atk}: {atk}")
            filtered_char['attack_data'] = {k: atk[k] for k in attack_required}
        else:
            filtered_char['attack_data'] = None

        # ---------- projectile_attack 필수 정보 ----------
        proj_list = []
        for proj in char.get('projectile_attack', []):
            if proj is None or not is_valid_attack(proj):
                continue
            missing_proj = [k for k in attack_required if k not in proj or proj[k] is None]
            if missing_proj:
                raise ValueError(f"Projectile missing required fields {missing_proj}: {proj}")
            proj_list.append({k: proj[k] for k in attack_required})
        filtered_char['projectile_attack'] = proj_list

        filtered_characters.append(filtered_char)

    # ---------- 시각화용 데이터 구조 반환 ----------
    return {
        'character_data': filtered_characters
    }


def visualize_frame(frame_data, ax):
    """
    한 프레임 데이터를 시각화합니다.
    캐릭터, HP/EN/Action, 공격 히트박스, 투사체를 표시합니다.
    공격 히트박스는 캐릭터 중심 좌표 기준으로 변환됩니다.

    Args:
        frame_data (dict): 한 프레임의 상태 액션 데이터
        ax (matplotlib.axes.Axes): 시각화를 위한 Axes 객체
    """

    frame_data = filter_frame_data(frame_data)  # 유효성 검증

    characters = frame_data['character_data']
    # projectiles = frame_data.get('projectile_data', [])

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
        speed_x, speed_y = char.get('speed_x', 0), char.get('speed_y', 0)

        # 캐릭터 사각형
        rect = patches.Rectangle(
            (left, top), right-left, bottom-top, linewidth=2,
            edgecolor='blue' if char['player_number'] else 'red', facecolor='none'
        )
        ax.add_patch(rect)

        # ---------- 시선 화살표 (front) ----------
        dx_front = 10 if front else -10
        y_front = y + 10  # 아래쪽으로 이동
        ax.arrow(x, y_front, dx_front, 0, head_width=8, head_length=8, fc='green', ec='green')

        # ---------- 속도 화살표 (speed_x, speed_y) ----------
        scale = 3  # 속도 스케일링
        if speed_x != 0 or speed_y != 0:
            ax.arrow(x, y, speed_x*scale, speed_y*scale, head_width=8, head_length=8, fc='orange', ec='orange')

        # ---------- 속도 텍스트 ----------
        speed_mag = math.sqrt(speed_x**2 + speed_y**2)
        # speed_text = f"speed=({speed_x:.1f},{speed_y:.1f})\n|v|={speed_mag:.2f}"
        speed_text = f"({speed_x:.1f},{speed_y:.1f})\n|v|={speed_mag:.2f}"
        ax.text(x, y-15, speed_text, color='orange', fontsize=8, ha='center',
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=3)  # 반투명 흰색 배경)
        )

        # ---------- HP / Energy / Action 텍스트 ----------
        ax.text(x, top-15, f"HP:{char['hp']}", color='red', fontsize=10, ha='center')
        ax.text(x, top-30, f"EN:{char['energy']}", color='blue', fontsize=10, ha='center')
        ax.text(x, bottom+15, f"Action:{char.get('action', '?')}", color='black', fontsize=10, ha='center')

        # 공격 & 투사체 공격 히트박스 표시
        attack_list = [char.get('attack_data')] + char.get('projectile_attack', [])
        for atk in attack_list:
            if atk is None or not is_valid_attack(atk):
                continue  # ✅ 유효하지 않은 공격/투사체는 제외

            hit_area = atk.get('current_hit_area')

            abs_left = hit_area['left']
            abs_right = hit_area['right']
            abs_top = hit_area['top']
            abs_bottom = hit_area['bottom']

            color = 'orange' if atk.get('player_number') else 'magenta'

            atk_rect = patches.Rectangle(
                (abs_left, abs_top),
                abs_right - abs_left,
                abs_bottom - abs_top,
                linewidth=1, edgecolor=color, facecolor='none', linestyle='--'
            )
            ax.add_patch(atk_rect)

            corner_x = [abs_left, abs_right, abs_right, abs_left]
            corner_y = [abs_top, abs_top, abs_bottom, abs_bottom]
            ax.plot(corner_x, corner_y, 'o', color=color, markersize=3)

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
                color=color, fontsize=8
            )

    ax.invert_yaxis()
    ax.grid(True)


if __name__ == "__main__":

    state_action_records_path = "../state_action_records/*.jsonl"
    state_action_records = glob(state_action_records_path)
    if not state_action_records:
        raise FileNotFoundError("No state-action records found.")

    # 첫 번째 파일 선택
    file_path = state_action_records[2]

    # debug_attack_projectile_lengths(file_path)
    # debug_attack_bboxes(file_path)

    # JSONL 한 줄씩 읽기
    with open(file_path, "r") as f:

        fig, ax = plt.subplots(figsize=(12, 8))

        for line in f:
            frame_data = json.loads(line)
            
            ax.cla()
            visualize_frame(frame_data, ax)
            plt.pause(0.1)
            # plt.pause(1.0)