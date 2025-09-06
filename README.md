# pyftg

An interface for implementing python AI in DareFightingICE

First, install `pyftg` with pip.
```sh
pip install pyftg
```

Initiate `Gateway` for connecting to DareFightingICE platform.
```py
from pyftg.socket.aio.gateway import Gateway
gateway = Gateway(port=31415)
```

Construct an agent and register it to gateway and then run the game by using following code.
```py
agent1 = KickAI()
agent2 = DisplayInfo()
gateway.register_ai("KickAI", agent1)
gateway.register_ai("DisplayInfo", agent2)
await gateway.run_game(["ZEN", "ZEN"], ["KickAI", "DisplayInfo"], game_num)
```

After all the process are done, please also close the gateway.
```py
await gateway.close()
```

Please refer to the examples provided in the `examples` directory for more information.

# For developer only
Please refer to this [link](https://twine.readthedocs.io/en/stable/).

1. Increase version number in pyproject.toml

1. Build project
```sh
python -m build
```
if the above command doesn't work due to ```no module named build``` error, install ```build``` library then try again
```sh
pip install build
```
3. Push project to pypi
```sh
twine upload dist/*
```

### 1. 실험 단계 (Experiment Pipeline)

#### 1.1 환경 분석 및 문제 정의
- FightingICE 환경 이해
- Observation, Action, Reward 구조 확인

#### 1.2 평가 및 개선
- **2-1. Observation 구조**  
  - Vector 단독  
  - Vector + MLP + CNN  

- **2-2. Action 구조 / Credit Assignment**  
  - 모션 수행 중 보상 지연 발생  
  - Delayed Reward, Reward Shaping 적용  

- **2-3. Reward 구조**  
  - 공격, 가드, 생존 등 상황 반영  

- **2-4. 학습**  
  - RL 모델 학습  

- **2-5. 평가**  
  - 다양한 상대와 대전  
  - 승률 및 전략 대응 능력 확인  

#### 1.3 결과 분석 및 개선
- 학습 곡선, 승률, 전략 다양성 확인
- Observation, Action, Reward 구조 개선

---

### 2. 연구 고려 사항

#### 2-1. Observation 구조
- Vector 단독 vs CNN 포함 구조
- 효율과 정보량 균형 고려

#### 2-2. Credit Assignment
- 행동과 보상 사이 시간 지연 존재
- Delayed Reward, Reward Shaping 적용

#### 2-3. 점진적 난이도 상승 학습
- Random → MCTS → Self Play
- 난이도 점진 상승(Curriculum Learning)

#### 2-4. 미래 예측 시스템 (MCTS)
- 미래 행동 평가 및 최적 행동 선택
- Self-Play, 난이도 조절, 전략 평가에 적용
