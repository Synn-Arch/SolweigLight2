"""solweig_scene_small 장면으로 thermal_comfort를 한 번 실행하고 걸린 시간을 출력한다.

사용 예:
    python run_solweig.py                        # 이 파일 옆의 solweig_scene_small 사용
    python run_solweig.py /path/to/other_scene   # 다른 장면 폴더 지정

먼저 `python make_small_scene.py`로 장면을 잘라 두어야 한다.
"""

import sys
import time
from pathlib import Path

from solweig_light import RuntimeOptions, runtime_options, thermal_comfort

SCENE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "solweig_scene_small"
SCENE = SCENE.expanduser().resolve()
if not (SCENE / "Building_DSM.tif").exists():
    sys.exit(f"장면 폴더에 Building_DSM.tif가 없습니다: {SCENE} (먼저 make_small_scene.py를 실행)")

print(f"[RUN] scene={SCENE} threads=4 tile_size=1024")
t0 = time.perf_counter()
with runtime_options(RuntimeOptions(
    memory_budget_bytes=6 * 1024**3,
    cpu_budget=4,
    workers=1,
    threads_per_worker=4,
    block_pixels=1024,
)):
    thermal_comfort(
        base_path=str(SCENE),
        selected_date_str="2020-08-13",
        landcover_filename="Landcover.tif",
        own_met_file=str(SCENE / "ownmet_Forcing_data.txt"),
        ERA_5_z0_find=False,
        use_uhi=False,
        tile_size=1024,
        overlap=0,
        save_tmrt=True,
    )
elapsed = time.perf_counter() - t0
print(f"[DONE] Duration: {elapsed/60:.1f}mins ({elapsed:.0f}seconds)  results: {SCENE / 'output_folder'}")
