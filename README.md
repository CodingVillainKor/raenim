# raenim
Manim utility packages for YouTube channel [Imcommit](https://www.youtube.com/@%EC%9E%84%EC%BB%A4%EB%B0%8B)


## How to install

1. Install raenim
```bash
pip install git+https://github.com/CodingVillainKor/raenim.git
```

2. import raenim
```python
from raenim import *
```

## How to use

### Scene: `Scene2D`, `Scene3D`

`Scene2D`(2D, `MovingCameraScene` 기반)와 `Scene3D`(3D, `ThreeDScene` 기반) 중 하나를 상속하여 씬을 만듭니다.

```python
class MyScene(Scene2D):
    def construct(self):
        c = Circle()
        self.playw(Create(c))           # play + wait (wait=1 기본)
        self.addw(c)                     # add + wait
        self.playwl(FadeIn(c), FadeIn(Square()))  # LaggedStart로 재생
        self.playw_return(c.animate.shift(RIGHT))  # there_and_back
        self.clear()                     # 모든 mobject FadeOut
        self.to_front(c)                 # 앞으로 가져오기
        self.play_camera(to=RIGHT*2, scale=1.5)   # 카메라 이동/줌
```

`Scene3D`에서는 `tilt_camera_horizontal(degree)`, `tilt_camera_vertical(degree)`, `move_camera_horizontally(degree)`, `move_camera_vertically(degree)` 등 카메라 유틸이 추가됩니다.

### Text: `CodeText`, `ListText`, `TextBox`, `TexBox`, `Words`, `RaeTex`

```python
ct = CodeText("print('hello')")          # 모노스페이스 코드 텍스트
lt = ListText("a", "b", "c")            # [a b c] 형태의 리스트 표시
tb = TextBox("hello")                   # 텍스트 + 박스 (tb.text, tb.box)
txb = TexBox(r"x^2")                    # LaTeX 수식 + 박스 (txb.tex, txb.box)

words = Words("hello world")
words.words[0]                           # "hello" 부분만 선택

rt = RaeTex(r"x`+`y`=`z")              # ` 기준으로 분할, 문자열로 인덱싱
rt["x"]                                 # "x" 부분 Mobject 반환
```

### Mobject: `SurroundingRect`, `Chainer`, `Joiner`, `BrokenLine`, `Pixel`, `PixelImage`, `Overlay`, `Mouse`

```python
sr = SurroundingRect()
sr.surround(some_mobject, buff_h=0.2, buff_w=0.2)  # mobject 감싸기

Chainer(obj1, obj2, obj3, chain_type="arrow")  # 객체 사이를 선/화살표로 연결
# chain_type: "plain"(Line), "dashedline"(DashedLine), "arrow"(Arrow)

BrokenLine(p1, p2, p3, arrow=True)     # 꺾인 선 (3개 이상 점 필요)

PixelImage("image.png")                 # 이미지를 픽셀 Mobject로 변환
PixelImage(np_array, pixel_size=0.1)    # numpy array도 가능
```

### Animation: `RWiggle`, `AMove`, `SkewedAnimations`, `AnchorToPoint`

```python
self.play(RWiggle(obj))                           # Perlin noise 기반 떨림
self.play(RWiggle(obj, amp=(0.2, 0.2, 0.0), speed=1.0))

self.play(AMove(obj, target_point=RIGHT * 3))     # 앤티시페이션(살짝 뒤로 갔다가) 이동

# 여러 애니메이션을 시차(skew)를 두고 재생
sa = SkewedAnimations(anims1, anims2)
for anim in sa:
    self.play(*anim)

# 그룹을 앵커 기준으로 특정 위치에 이동
self.play(AnchorToPoint(group, dest=RIGHT*2, anchor=group[0]))
```

### Neural Network: `Linear`, `MLP`, `Tensor`, `Activation`, `forward_prop`, `backward_prop`

```python
linear = Linear(3, 2)                   # 3→2 단층 네트워크 시각화
mlp = MLP(4, 3, 2)                      # 4→3→2 MLP 시각화

t = Tensor(5)                           # 5차원 텐서 (원형)
t = Tensor(5, shape="square")           # 5차원 텐서 (사각형)
self.play(t.to_numbers())               # 랜덤 숫자로 변환

forward_prop(mlp, self)                 # 순전파 애니메이션
backward_prop(mlp, self)                # 역전파 애니메이션

act = Activation("tanh")                # 활성화 함수 시각화 ("tanh", "relu")
```

### Script: `PythonCode`

```python
code = PythonCode("example.py")         # 파이썬 코드 시각화

code(3)                                  # 3번째 줄 Mobject
code(2, 5)                               # 2~5번째 줄 슬라이스

code.text_slice(3, "print")             # 3번째 줄에서 "print" 부분 선택
hl_in, hl_out = code.highlight(3, "x")  # 하이라이트 (Write → FadeOut)

# 실행 순서대로 한 줄씩 하이라이트
for anim in code.exec():
    self.play(anim)
```

### Matrix: `Mat`

```python
Mat.zeros(3, 3)                          # 0 행렬
Mat.ones(2, 4)                           # 1 행렬
Mat.eye(3)                               # 단위 행렬
Mat.randn(2, 3)                          # 랜덤 행렬
```

### FileSystem: `FileSystem`, `File`, `Folder`, `FileIcon`, `FolderIcon`

```python
fs = FileSystem(
    folders=["src", "tests"],
    files=["main.py", "README.md"],
    tag="my_project"
)
fs.folders[0]                            # 첫 번째 폴더 (icon + text)
fs.files[1]                              # 두 번째 파일 (icon + text)
```

### Git: `branch`, `new_commit`, `get_commit`

```python
commits = branch(n_commits=3)            # 커밋 3개짜리 브랜치 생성
c = get_commit()                         # 단일 커밋 노드
new_c, line = new_commit(c)             # 기존 커밋에서 새 커밋 추가
```

### 기타

- `MINT` : 민트색 커스텀 컬러 (`#00DDAA`)
- `Logo` : 임커밋 로고 Mobject
- `MONO_FONT` : OS별 자동 선택 모노스페이스 폰트
