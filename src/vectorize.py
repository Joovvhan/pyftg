import numpy as np
from glob import glob
import json

from visualize_state_action_records import filter_frame_data

def flatten_dict_to_vector_with_keys(d, parent_key=""):
    """
    중첩 dict/list를 완전히 펴서 1차원 벡터와 변수명 리스트를 반환합니다.
    
    숫자/불린 값만 포함, 변환 불가 값은 print.
    
    Returns:
        vector (list of float)
        keys (list of str): vector[i]가 어떤 key에서 왔는지
    """
    vector = []
    keys = []

    if isinstance(d, dict):
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            v_vec, v_keys = flatten_dict_to_vector_with_keys(v, new_key)
            vector.extend(v_vec)
            keys.extend(v_keys)
    elif isinstance(d, list):
        for idx, item in enumerate(d):
            new_key = f"{parent_key}[{idx}]"
            v_vec, v_keys = flatten_dict_to_vector_with_keys(item, new_key)
            vector.extend(v_vec)
            keys.extend(v_keys)
    else:
        try:
            if d is None:
                vector.append(0.0)
            elif isinstance(d, bool):
                vector.append(float(d))
            else:
                vector.append(float(d))
            keys.append(parent_key)
        except Exception:
            print(f"Failed to convert to float at key '{parent_key}': {d}")
            # 건너뛰고 vector/keys에 추가하지 않음

    return vector, keys

if __name__ == "__main__":

    state_action_records_path = "../state_action_records/*.jsonl"
    state_action_records = glob(state_action_records_path)
    if not state_action_records:
        raise FileNotFoundError("No state-action records found.")

    # 첫 번째 파일 선택
    file_path = state_action_records[2]

    with open(file_path, "r") as f:

        for line in f:
            frame_data = json.loads(line)

            frame_data = filter_frame_data(frame_data)

            vec, var_names = flatten_dict_to_vector_with_keys(frame_data)
            print(len(vec), len(var_names))
            # print(vec)
            # print(var_names)

            # break
